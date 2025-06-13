"""
Base Workflow Agent that coordinates multiple specialized agents
"""

import os
import time
import json
from typing import List, Dict, Any
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from groq import RateLimitError
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain_groq import ChatGroq
from langchain_core.memory import BaseMemory
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage

class BaseWorkflowAgent:
    """Base class for workflow coordination"""
    
    def __init__(
        self,
        model_name: str = "llama-3.1-8b-instant",
        temperature: float = 0.7,
        **kwargs
    ):
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = kwargs.get('max_tokens', 1024)
        self.verbose = kwargs.get('verbose', True)
        
        # Initialize components
        self.llm = self._init_llm()
        self.memory = self._init_memory()
        self.tools = self._get_tools()
        self.agent_executor = self._create_agent()
        
    @retry(
        retry=retry_if_exception_type(RateLimitError),
        wait=wait_exponential(multiplier=1, min=4, max=60),
        stop=stop_after_attempt(3)
    )
    def _init_llm(self):
        return ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name=self.model_name,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
    
    def _init_memory(self) -> BaseMemory:
        return ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="output"
        )
    
    def _get_tools(self) -> List[Tool]:
        """Get workflow coordination tools"""
        return [
            Tool(
                name="delegate_task",
                func=self._delegate_task,
                description="Delegate a task to a specialized agent"
            ),
            Tool(
                name="combine_results",
                func=self._combine_results,
                description="Combine results from multiple agents"
            ),
            Tool(
                name="validate_output",
                func=self._validate_output,
                description="Validate the output meets requirements"
            )
        ]
    
    def _create_agent(self) -> AgentExecutor:
        """Create the agent executor"""
        prompt = PromptTemplate(
            template="""You are a workflow coordination agent that helps manage and execute complex tasks.
            You have access to the following tools:
            
            {tools}
            
            Tool Names: {tool_names}
            
            Use these tools to help accomplish the user's request.
            
            Previous conversation history:
            {chat_history}
            
            User's request: {input}
            
            Let's approach this step by step:
            1) First, understand what needs to be done
            2) Break it down into subtasks if needed
            3) Use the appropriate tools to execute each part
            4) Validate and combine the results
            
            When using tools, follow this format EXACTLY:
            Thought: I need to do X
            Action: tool_name
            Action Input: the input to the tool
            Observation: the result of the tool
            ... (this Thought/Action/Action Input/Observation can repeat N times)
            Thought: I am finished
            Final Answer: the final output
            
            {agent_scratchpad}""",
            input_variables=["input", "chat_history", "agent_scratchpad", "tools", "tool_names"]
        )
        
        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=self.verbose,
            handle_parsing_errors=True,
            max_iterations=5  # Increased iterations for more complex workflows
        )
    
    @retry(
        retry=retry_if_exception_type(RateLimitError),
        wait=wait_exponential(multiplier=1, min=4, max=60),
        stop=stop_after_attempt(3)
    )
    def _llm_call(self, prompt: str, system_message: str = None, json_output: bool = False) -> Any:
        """Make a call to the LLM, optionally parsing JSON output."""
        messages = []
        if system_message:
            messages.append(SystemMessage(content=system_message))
        
        if json_output:
            prompt += "\n\nReturn your response as a valid JSON object."

        messages.append(HumanMessage(content=prompt))
        
        response = self.llm.invoke(messages)
        content = response.content
        
        if json_output:
            try:
                # The response might be inside ```json ... ```
                if content.strip().startswith("```json"):
                    content = content.strip()[7:-4].strip()
                return json.loads(content)
            except json.JSONDecodeError:
                # Fallback for when JSON parsing fails
                return {"error": "Failed to parse LLM response as JSON", "response": content}
        
        return content
    
    @retry(
        retry=retry_if_exception_type(RateLimitError),
        wait=wait_exponential(multiplier=1, min=4, max=60),
        stop=stop_after_attempt(3)
    )
    def _delegate_task(self, task_spec: str) -> str:
        """Delegate a task to appropriate specialized agent"""
        try:
            # Parse the task specification
            task_type = self._llm_call(
                prompt=f"What type of task is this? Options: web_research, analysis, synthesis\nTask: {task_spec}",
                system_message="You are a task classifier. Respond with ONLY one of the following: web_research, analysis, synthesis"
            ).strip().lower()
            
            # Execute the task based on type
            if task_type == "web_research":
                result = self._llm_call(
                    prompt=f"Perform web research on: {task_spec}",
                    system_message="You are a web researcher. Search the web and provide relevant information."
                )
                return {"type": "web_research", "result": result}
            
            elif task_type == "analysis":
                result = self._llm_call(
                    prompt=f"Analyze this content: {task_spec}",
                    system_message="You are a content analyzer. Analyze the content and provide insights."
                )
                return {"type": "analysis", "result": result}
            
            elif task_type == "synthesis":
                result = self._llm_call(
                    prompt=f"Synthesize this information: {task_spec}",
                    system_message="You are an information synthesizer. Combine and summarize the information."
                )
                return {"type": "synthesis", "result": result}
            
            else:
                return {"type": "unknown", "result": "Task type not recognized"}
            
        except Exception as e:
            return {"type": "error", "result": str(e)}
    
    @retry(
        retry=retry_if_exception_type(RateLimitError),
        wait=wait_exponential(multiplier=1, min=4, max=60),
        stop=stop_after_attempt(3)
    )
    def _combine_results(self, results: List[str]) -> str:
        """Combine results from multiple agents"""
        try:
            # Convert results to string if they're not already
            results_str = str(results)
            
            # Combine the results
            combined = self._llm_call(
                prompt=f"Combine these results into a coherent output:\n{results_str}",
                system_message="You are a results integrator. Combine the results into a coherent and well-structured output."
            )
            
            return {"status": "success", "combined_results": combined}
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    @retry(
        retry=retry_if_exception_type(RateLimitError),
        wait=wait_exponential(multiplier=1, min=4, max=60),
        stop=stop_after_attempt(3)
    )
    def _validate_output(self, output: str) -> bool:
        """Validate if output meets requirements"""
        try:
            # Validate the output
            validation = self._llm_call(
                prompt=f"Validate this output meets quality requirements:\n{output}",
                system_message="You are a quality validator. Check if the output is complete, coherent, and meets quality standards. Respond with ONLY 'valid' or 'invalid' followed by a brief reason."
            )
            
            is_valid = validation.lower().startswith("valid")
            reason = validation.split(" ", 1)[1] if " " in validation else ""
            
            return {
                "status": "success",
                "is_valid": is_valid,
                "reason": reason
            }
            
        except Exception as e:
            return {
                "status": "error",
                "is_valid": False,
                "error": str(e)
            }
    
    @retry(
        retry=retry_if_exception_type(RateLimitError),
        wait=wait_exponential(multiplier=1, min=4, max=60),
        stop=stop_after_attempt(3)
    )
    def run(self, input_text: str) -> Dict[str, Any]:
        """Run the workflow agent"""
        return self.agent_executor.invoke(
            {"input": input_text}
        ) 