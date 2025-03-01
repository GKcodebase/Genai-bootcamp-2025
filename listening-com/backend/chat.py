import os
from dotenv import load_dotenv
import boto3
import streamlit as st
from typing import Optional, Dict, Any

# Load environment variables from .env file
load_dotenv()

# Model ID
MODEL_ID = "amazon.nova-micro-v1:0"

class BedrockChat:
    def __init__(self, model_id: str = MODEL_ID):
        """Initialize Bedrock chat client"""
        self.bedrock_client = boto3.client(
            'bedrock-runtime',
            region_name="us-east-1",
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        self.model_id = model_id
        self.prompts = {
            'translate_to_english': """
                Translate the following Japanese text to English:
                {text}
                Please provide:
                1. Translation
                2. Word-by-word breakdown
                3. Cultural notes (if any)
            """,
            'translate_to_japanese': """
                Translate the following English text to Japanese:
                {text}
                Please provide:
                1. Translation in Kanji/Hiragana
                2. Romaji
                3. Word-by-word breakdown
                4. Usage examples
            """,
            'kanji_info': """
                Analyze the following Japanese text:
                {text}
                Please provide:
                1. Kanji breakdown
                2. Readings (On'yomi and Kun'yomi)
                3. Common compounds
                4. Stroke order description
                5. Example sentences
            """,
            'language_analysis': """
                Analyze the following Japanese text:
                {text}
                Please provide:
                1. Grammar points used
                2. Level (N5-N1)
                3. Similar expressions
                4. Common usage contexts
            """
        }

    def generate_response(self, message: str, response_type: str = 'translate_to_english', 
                         inference_config: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """Generate a response using Amazon Bedrock"""
        if inference_config is None:
            inference_config = {"temperature": 0.7}

        # Get the appropriate prompt template
        prompt_template = self.prompts.get(response_type, self.prompts['translate_to_english'])
        
        # Format the prompt with the message
        formatted_prompt = prompt_template.format(text=message)

        messages = [{
            "role": "user",
            "content": [{"text": formatted_prompt}]
        }]

        try:
            response = self.bedrock_client.converse(
                modelId=self.model_id,
                messages=messages,
                inferenceConfig=inference_config
            )
            return response['output']['message']['content'][0]['text']
            
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            return None

if __name__ == "__main__":
    chat = BedrockChat()
    while True:
        user_input = input("You: ")
        if user_input.lower() == '/exit':
            break
        response = chat.generate_response(user_input)
        print("Bot:", response)
