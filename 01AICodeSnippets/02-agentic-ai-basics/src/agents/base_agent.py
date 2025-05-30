from typing import List, Dict, Any
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

class BaseAgent:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
            
        self.api_key = api_key
        self.base_url = "https://api.groq.com/openai/v1"
        self.tools = self._get_default_tools()

    def _get_default_tools(self) -> List[Dict]:
        # Will be implemented in specific agents
        return []

    def _create_prompt(self, task: str) -> str:
        tools_description = "\n".join([
            f"- {tool['name']}: {tool['description']}"
            for tool in self.tools
        ])
        
        return f"""You are a helpful AI assistant that can use tools to accomplish tasks.
        
        Available tools:
        {tools_description}
        
        Task: {task}
        
        Think through this step-by-step:
        1) What needs to be done
        2) What tools would help
        3) Execute the plan
        """

    def run(self, task: str) -> Dict[str, Any]:
        prompt = self._create_prompt(task)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "messages": [{
                "role": "user",
                "content": prompt
            }],
            "model": "llama3-8b-8192",
            "temperature": 0.7
        }
        
        chat_completions_url = f"{self.base_url}/chat/completions"

        try:
            with httpx.Client() as client:
                response = client.post(
                    chat_completions_url,
                    headers=headers,
                    json=data,
                    timeout=30.0
                )
                
                # Debug: Print response details if there's an error
                if response.status_code != 200:
                    print(f"Status Code: {response.status_code}")
                    print(f"Response Text: {response.text}")
                
                response.raise_for_status()
                result = response.json()
                
            return {
                "output": result["choices"][0]["message"]["content"]
            }
        except Exception as e:
            print(f"Error occurred: {e}")
            print(f"URL used: {chat_completions_url}")
            raise 