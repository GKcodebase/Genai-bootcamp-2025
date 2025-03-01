import boto3
import json
from typing import Dict, List, Optional
from dotenv import load_dotenv
import os
import chromadb
import tempfile

class InteractiveLearning:
    def __init__(self, collection_name: str = "jlptn5-listening-comprehension"):
        """Initialize Bedrock client, Polly client and ChromaDB"""
        load_dotenv()
        
        # Get the absolute path to the project root
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.chromadb_path = os.path.join(self.project_root, "backend", "data", "chromadb")
        
        # Initialize ChromaDB client
        self.chroma_client = chromadb.PersistentClient(path=self.chromadb_path)
        
        try:
            self.collection = self.chroma_client.get_collection(collection_name)
        except:
            self.collection = self.chroma_client.create_collection(collection_name)

        # Initialize AWS clients with proper configuration
        aws_config = {
            'region_name': "us-east-1",
            'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
            'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY')
        }
        
        self.bedrock_client = boto3.client('bedrock-runtime', **aws_config)
        self.polly_client = boto3.client('polly', **aws_config)
        
        # Configure Polly voice settings
        self.voice_config = {
            'VoiceId': 'Mizuki',  # Japanese voice
            'Engine': 'standard',  # Use standard engine instead of neural
            'LanguageCode': 'ja-JP'
        }
        
    def get_questions_by_section(self, section_num: int) -> List[Dict]:
        """Retrieve questions from ChromaDB by section and pre-generate audio"""
        try:
            results = self.collection.query(
                query_texts=[""],
                where={"section": str(section_num)},
                n_results=10
            )
            
            questions = []
            for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
                question = self._parse_question(doc)
                if question:
                    # Add metadata
                    question['metadata'] = metadata
                    
                    # Pre-generate audio for each text section
                    question['audio'] = {}
                    
                    try:
                        if 'Introduction' in question:
                            question['audio']['Introduction'] = self.generate_audio(question['Introduction'])
                            question['audio']['Conversation'] = self.generate_audio(question['Conversation'])
                            question['audio']['Question'] = self.generate_audio(question['Question'])
                        else:
                            question['audio']['Situation'] = self.generate_audio(question['Situation'])
                            question['audio']['Question'] = self.generate_audio(question['Question'])
                    except Exception as e:
                        print(f"Error generating audio for question: {str(e)}")
                        # Continue even if audio generation fails
                        pass
                    
                    questions.append(question)
            
            return questions
            
        except Exception as e:
            print(f"Error retrieving questions: {str(e)}")
            return []

    def _parse_question(self, raw_question: str) -> Dict:
        """Parse raw question text into structured format"""
        try:
            question = {}
            current_key = None
            current_value = []
            
            lines = raw_question.strip().split('\n')
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                if line.startswith(('Introduction:', 'Conversation:', 'Situation:', 'Question:', 'Options:')):
                    if current_key:
                        question[current_key] = ' '.join(current_value) if current_key != 'Options' else current_value
                    current_key = line.split(':')[0]
                    current_value = []
                elif current_key:
                    if current_key == 'Options' and line[0].isdigit() and line[1] == '.':
                        current_value.append(line[2:].trip())
                    else:
                        current_value.append(line)
            
            if current_key:
                question[current_key] = ' '.join(current_value) if current_key != 'Options' else current_value
                
            return question
        except Exception as e:
            print(f"Error parsing question: {str(e)}")
            return None

    def generate_feedback(self, question: Dict, selected_answer: int) -> Dict:
        """Generate feedback using Bedrock"""
        prompt = self._create_feedback_prompt(question, selected_answer)
        
        try:
            response = self.bedrock_client.converse(
                modelId=self.model_id,
                messages=[{
                    "role": "user",
                    "content": [{"text": prompt}]
                }],
                inferenceConfig={"temperature": 0.7}
            )
            
            feedback_text = response['output']['message']['content'][0]['text']
            return json.loads(feedback_text)
        except Exception as e:
            print(f"Error generating feedback: {str(e)}")
            return {
                "correct": False,
                "explanation": "Unable to generate feedback. Please try again.",
                "correct_answer": 1
            }

    def _create_feedback_prompt(self, question: Dict, selected_answer: int) -> str:
        """Create prompt for feedback generation"""
        prompt = """Analyze this JLPT question and provide feedback for the selected answer.
        Return the response in this JSON format:
        {
            "correct": boolean,
            "explanation": "explanation in both Japanese and English",
            "correct_answer": number (1-4)
        }
        
        Question:
        """
        
        for key, value in question.items():
            if key != 'metadata':
                if isinstance(value, list):
                    prompt += f"\n{key}:\n" + "\n".join(f"{i+1}. {opt}" for i, opt in enumerate(value))
                else:
                    prompt += f"\n{key}: {value}"
        
        prompt += f"\n\nSelected answer: {selected_answer}"
        return prompt

    def generate_audio(self, text: str) -> Optional[bytes]:
        """Generate audio using Amazon Polly"""
        if not text or not text.strip():
            return None
            
        try:
            # Add SSML pauses for better speech rhythm
            ssml_text = f"""<speak>
                <prosody rate="slow">
                    {text}
                </prosody>
            </speak>"""
            
            response = self.polly_client.synthesize_speech(
                Text=ssml_text,
                TextType='ssml',
                OutputFormat='mp3',
                **self.voice_config
            )
            
            if "AudioStream" in response:
                return response["AudioStream"].read()
            return None
            
        except Exception as e:
            print(f"Error generating audio: {str(e)}")
            return None