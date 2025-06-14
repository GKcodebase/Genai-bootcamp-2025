import os
import time
import random
import logging
from typing import Dict, Any, List, Optional
from google.cloud import aiplatform
from google.generativeai import GenerativeModel
import google.generativeai as genai
from google.api_core import retry_async
from google.api_core.exceptions import ResourceExhausted

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GoogleAgent:
    """Google Vertex AI Agent implementation using Agentic SDK features."""
    
    def __init__(
        self,
        project_id: Optional[str] = None,
        location: str = "us-central1",
        model_name: str = "gemini-1.5-flash"
    ):
        """Initialize the Google Agent.
        
        Args:
            project_id: Google Cloud project ID
            location: Google Cloud location
            model_name: Name of the Gemini model to use
        """
        # Get credentials from environment
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")
            
        # Initialize Vertex AI
        aiplatform.init(
            project=self.project_id,
            location=location
        )
        
        # Configure Gemini API
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        genai.configure(api_key=api_key)
        
        # Store model name without prefix
        self.model_name = model_name.replace("models/", "")
        
        # Initialize the model with agentic capabilities
        self.model = GenerativeModel(
            self.model_name,
            generation_config={
                "temperature": 0.7,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 1024,
            }
        )
        
        # Agent state
        self.state = {
            "conversation_history": [],
            "tool_results": {},
            "current_plan": None,
            "execution_status": None,
            "quota_info": {
                "requests_this_minute": 0,
                "last_request_time": 0,
                "daily_requests": 0
            }
        }
        
        # Rate limiting settings
        self.last_request_time = 0
        self.min_request_interval = 5.0
        self.max_retries = 3
        self.base_delay = 10.0
        
        logger.info(f"Initialized Google Agent with model: {self.model_name}")
        
    def _wait_for_rate_limit(self):
        """Wait if necessary to respect rate limits."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last_request
            sleep_time += random.uniform(0, 1.0)  # Increased jitter
            logger.info(f"Rate limiting: Waiting {sleep_time:.1f} seconds before next request")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
        self.state["quota_info"]["requests_this_minute"] += 1
        self.state["quota_info"]["daily_requests"] += 1
        self.state["quota_info"]["last_request_time"] = current_time
    
    def _handle_quota_error(self, e: Exception, attempt: int) -> None:
        """Handle quota exceeded errors with exponential backoff."""
        if isinstance(e, ResourceExhausted):
            delay = self.base_delay * (2 ** attempt)
            delay += random.uniform(0, 2.0)  # Increased jitter
            logger.warning(
                f"Quota exceeded (attempt {attempt + 1}/{self.max_retries}). "
                f"Waiting {delay:.1f} seconds. "
                f"Requests this minute: {self.state['quota_info']['requests_this_minute']}, "
                f"Daily requests: {self.state['quota_info']['daily_requests']}"
            )
            time.sleep(delay)
    
    def _create_agent_prompt(self, task: str, tools: Optional[List[Dict[str, Any]]] = None) -> str:
        """Create a structured prompt for the agent."""
        prompt = f"""You are an AI agent with the following capabilities:

Task: {task}

Current State:
- Conversation History: {len(self.state['conversation_history'])} messages
- Tool Results: {len(self.state['tool_results'])} results
- Current Plan: {self.state['current_plan'] or 'None'}
- Execution Status: {self.state['execution_status'] or 'Not Started'}

"""
        if tools:
            prompt += "Available Tools:\n"
            for tool in tools:
                prompt += f"- {tool['name']}: {tool['description']}\n"
                prompt += "  To use this tool, respond with: USE_TOOL: {tool_name} {parameters}\n"
        
        prompt += "\nPlease follow these steps:\n"
        prompt += "1. Analyze the task and current state\n"
        prompt += "2. Create or update the execution plan\n"
        prompt += "3. Execute the plan using available tools\n"
        prompt += "4. Provide a detailed response\n"
        
        return prompt
    
    async def run_agent(
        self,
        task: str,
        tools: Optional[List[Dict[str, Any]]] = None,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """Run the agent on a task with agentic capabilities."""
        attempt = 0
        while attempt < self.max_retries:
            try:
                # Wait for rate limit
                self._wait_for_rate_limit()
                
                # Create structured prompt
                prompt = self._create_agent_prompt(task, tools)
                if context:
                    prompt += f"\nAdditional Context: {context}\n"
                
                logger.info(f"Running agent task: {task[:50]}...")
                
                # Generate response with agentic capabilities
                response = self.model.generate_content(prompt)
                
                # Update agent state
                self.state["current_plan"] = "Task completed"
                self.state["execution_status"] = "Success"
                
                logger.info("Task completed successfully")
                
                return {
                    "response": response.text,
                    "metadata": {
                        "model": self.model_name,
                        "project_id": self.project_id,
                        "tools_used": tools,
                        "agent_state": self.state
                    }
                }
                
            except ResourceExhausted as e:
                attempt += 1
                if attempt >= self.max_retries:
                    logger.error(f"Max retries exceeded. Last error: {str(e)}")
                    raise Exception(f"Max retries ({self.max_retries}) exceeded. Last error: {str(e)}")
                self._handle_quota_error(e, attempt)
            except Exception as e:
                self.state["execution_status"] = "Error"
                logger.error(f"Error running agent: {str(e)}")
                raise Exception(f"Error running agent: {str(e)}")
    
    async def run_agent_with_memory(
        self,
        task: str,
        conversation_history: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Run the agent with conversation memory and agentic capabilities."""
        attempt = 0
        while attempt < self.max_retries:
            try:
                # Wait for rate limit
                self._wait_for_rate_limit()
                
                # Update agent state with conversation history
                self.state["conversation_history"] = conversation_history
                
                # Convert conversation history to Gemini format
                gemini_history = []
                for msg in conversation_history:
                    gemini_history.append({
                        "parts": [{"text": msg["content"]}],
                        "role": msg["role"]
                    })
                
                # Create structured prompt
                prompt = self._create_agent_prompt(task, tools)
                
                logger.info(f"Running agent with memory. Task: {task[:50]}...")
                
                # Prepare the conversation with agentic capabilities
                chat = self.model.start_chat(history=gemini_history)
                
                # Generate response
                response = chat.send_message(prompt)
                
                # Update agent state
                self.state["current_plan"] = "Task completed with memory"
                self.state["execution_status"] = "Success"
                
                logger.info("Task with memory completed successfully")
                
                return {
                    "response": response.text,
                    "metadata": {
                        "model": self.model_name,
                        "project_id": self.project_id,
                        "tools_used": tools,
                        "conversation_length": len(conversation_history) + 1,
                        "agent_state": self.state
                    }
                }
                
            except ResourceExhausted as e:
                attempt += 1
                if attempt >= self.max_retries:
                    logger.error(f"Max retries exceeded. Last error: {str(e)}")
                    raise Exception(f"Max retries ({self.max_retries}) exceeded. Last error: {str(e)}")
                self._handle_quota_error(e, attempt)
            except Exception as e:
                self.state["execution_status"] = "Error"
                logger.error(f"Error running agent with memory: {str(e)}")
                raise Exception(f"Error running agent with memory: {str(e)}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Get agent information as dictionary."""
        return {
            "name": "Google Vertex AI Agent",
            "model": self.model_name,
            "project_id": self.project_id,
            "state": self.state
        } 