import boto3
import json
from typing import Dict, List, Optional
from dotenv import load_dotenv
import os
import chromadb
from .rag import RAGSystem

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
        
        # Configure available voices
        self.voice_configs = {
            'female': {
                'VoiceId': 'Mizuki',
                'Engine': 'standard',
                'LanguageCode': 'ja-JP'
            },
            'male': {
                'VoiceId': 'Takumi',
                'Engine': 'standard',
                'LanguageCode': 'ja-JP'
            },
            'neural_female': {
                'VoiceId': 'Kazuha',
                'Engine': 'neural',
                'LanguageCode': 'ja-JP'
            }
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
                
                print(f"Processing line: {line}")  # Debug line
                
                if line.startswith('Correct Answer:'):
                    question['correct_answer'] = int(line.replace('Correct Answer:', '').strip())
                    continue
                    
                if ':' in line:
                    key_markers = ['Situation:', 'Question:', 'Options:', 'Introduction:', 'Conversation:']
                    for marker in key_markers:
                        if line.startswith(marker):
                            if current_key:
                                if current_key == 'Options':
                                    question[current_key] = current_value[:4]  # Limit to 4 options
                                else:
                                    question[current_key] = ' '.join(current_value).strip()
                            current_key = marker[:-1]
                            current_value = [line[len(marker):].strip()]
                            break
                    else:
                        if current_key:
                            current_value.append(line)
                elif current_key:
                    if current_key == 'Options' and line[0].isdigit() and line[1] == '.':
                        if len(current_value) <= 4:  # Only add if we have less than 4 options
                            current_value.append(line[2:].strip())
                    else:
                        current_value.append(line)
            
            # Save the last key-value pair
            if current_key:
                if current_key == 'Options':
                    question[current_key] = current_value[1:5]  # Ensure exactly 4 options
                else:
                    question[current_key] = ' '.join(current_value).strip()
            
            # Validate parsed question
            required_keys = ['Question', 'Options', 'correct_answer']
            missing_keys = [key for key in required_keys if key not in question]
            if missing_keys:
                print(f"Missing required keys: {missing_keys}")
                return None
            
            # # Ensure exactly 4 options
            # if len(question['Options']) != 4:
            #     print("Question must have exactly 4 options")
            #     return None
            
            # Validate correct_answer is between 1 and 4
            if not (1 <= question['correct_answer'] <= 4):
                print("Correct answer must be between 1 and 4")
                return None
                
            return question
            
        except Exception as e:
            print(f"Error parsing question: {str(e)}")
            import traceback
            print(traceback.format_exc())
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

    def generate_audio_for_question(self, question: Dict) -> Dict[str, Dict[str, bytes]]:
        """Generate audio for all parts of the question with different voices"""
        audio_data = {}
        
        try:
            # Generate audio for situation/introduction with female voice
            if 'Introduction' in question:
                audio_data['Introduction'] = {
                    'audio': self.generate_audio(question['Introduction'], 'female'),
                    'voice': 'female'
                }
                # Generate conversation with alternating voices
                conversation_parts = question['Conversation'].split('\n')
                conversation_audio = []
                for i, part in enumerate(conversation_parts):
                    voice = 'male' if i % 2 == 0 else 'female'
                    audio = self.generate_audio(part, voice)
                    if audio:
                        conversation_audio.append({'audio': audio, 'voice': voice})
                audio_data['Conversation'] = conversation_audio
            else:
                audio_data['Situation'] = {
                    'audio': self.generate_audio(question['Situation'], 'neural_female'),
                    'voice': 'neural_female'
                }
            
            # Generate question and options audio
            audio_data['Question'] = {
                'audio': self.generate_audio(question['Question'], 'female'),
                'voice': 'female'
            }
            
            # Generate audio for options
            options_audio = []
            for opt in question['Options']:
                audio = self.generate_audio(opt, 'male')
                if audio:
                    options_audio.append({'audio': audio, 'voice': 'male'})
            audio_data['Options'] = options_audio
            
            return audio_data
            
        except Exception as e:
            print(f"Error generating audio: {str(e)}")
            return {}

    def generate_audio(self, text: str, voice_type: str = 'female') -> Optional[bytes]:
        """Generate audio using Amazon Polly with specified voice"""
        if not text or not text.strip():
            return None
            
        try:
            voice_config = self.voice_configs.get(voice_type, self.voice_configs['female'])
            ssml_text = f"""<speak>
                <prosody rate="slow">
                    {text}
                </prosody>
            </speak>"""
            
            response = self.polly_client.synthesize_speech(
                Text=ssml_text,
                TextType='ssml',
                OutputFormat='mp3',
                **voice_config
            )
            
            if "AudioStream" in response:
                return response["AudioStream"].read()
            return None
            
        except Exception as e:
            print(f"Error generating audio: {str(e)}")
            return None

    def _invoke_bedrock(self, prompt: str) -> Optional[str]:
        """Helper method to invoke Bedrock API with Nova model"""
        try:
            # Format request according to Nova model requirements
            messages = [{
                "role": "user",
                "content": [{"text": prompt}]
            }]

            # Set inference configuration
            inference_config = {
                "temperature": 0.7,
                "topP": 0.999,
                "maxTokens": 2000,
                "stopSequences": ["\n\nHuman:", "\n\nAssistant:"]
            }

            print("Sending request to Bedrock...")
            response = self.bedrock_client.converse(
                modelId="amazon.nova-lite-v1:0",
                messages=messages,
                inferenceConfig=inference_config
            )
            
            print(f"Raw response: {response}")  # Debug line
            
            # Extract the generated text from response
            if 'output' in response and 'message' in response['output']:
                return response['output']['message']['content'][0]['text']
            return None
            
        except Exception as e:
            print(f"Error invoking Bedrock Nova: {str(e)}")
            print(f"Request body: {messages}")  # Debug line
            return None

    def generate_similar_question(self, section_num: int, topic: str) -> Dict:
        """Generate a new question similar to existing ones on a given topic"""
        try:
            print("Starting question generation process...")
            
            # Create RAG instance
            rag = RAGSystem()
            print("RAG system initialized")
            
            # Query similar questions using RAG
            print(f"Querying for topic: {topic}")
            results = rag.query_similar(topic)
            
            filtered_questions = []
            if results and results['documents'][0]:
                print(f"Found {len(results['documents'][0])} similar questions")
                
                # Filter results by section
                for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
                    print(f"Processing document with metadata: {metadata}")
                    if metadata['section'] == str(section_num):
                        question = self._parse_question(doc)
                        if question:
                            filtered_questions.append(question)
            
            # If no questions found, generate from scratch using Nova
            if not filtered_questions:
                print("No existing questions found, generating from scratch...")
                template = self._get_question_template(section_num)
                
                prompt = f"""以下のフォーマットでJLPT N5レベルの{topic}に関する質問を作成してください。
                必ず4つの選択肢を用意し、正解の番号も明記してください。

                {template}
                
                Requirements:
                - Keep vocabulary and grammar at JLPT N5 level
                - Make the conversation natural and practical
                - Include exactly 4 options
                - Add the correct answer number (1-4) after options
                - Use simple, everyday situations
                - All text must be in Japanese only
                
                New Question:"""
                
                print("Calling Bedrock Nova for question generation...")
                response = self._invoke_bedrock(prompt)
                if response:
                    return self._parse_question(response)
                return None
            
            # Continue with existing logic for similar questions...
            print(f"Filtered to {len(filtered_questions)} questions for section {section_num}")
            
            # Rest of the method remains the same...
            
        except Exception as e:
            print(f"Error generating similar question: {str(e)}")
            import traceback
            print("Full traceback:")
            print(traceback.format_exc())
            return None

    def _get_question_template(self, section_num: int) -> str:
        """Get template for question generation based on section number"""
        if section_num == 2:
            return """Introduction: [短い状況説明]
Conversation: [2人の会話]
Question: [質問]
Options:
1. [選択肢1]
2. [選択肢2]
3. [選択肢3]
4. [選択肢4]
Correct Answer: [1-4の数字]"""
        else:
            return """Situation: [状況説明]
Question: [質問]
Options:
1. [選択肢1]
2. [選択肢2]
3. [選択肢3]
4. [選択肢4]
Correct Answer: [1-4の数字]"""

    def _format_section_2_question(self, idx: int, q: Dict) -> str:
        """Format a section 2 question for the context"""
        result = f"Example {idx}:\n"
        result += f"Introduction: {q.get('Introduction', '')}\n"
        result += f"Conversation: {q.get('Conversation', '')}\n"
        result += f"Question: {q.get('Question', '')}\n"
        if 'Options' in q:
            result += "Options:\n"
            for i, opt in enumerate(q['Options'], 1):
                result += f"{i}. {opt}\n"
        result += "\n"
        return result

    def _format_section_3_question(self, idx: int, q: Dict) -> str:
        """Format a section 3 question for the context"""
        result = f"Example {idx}:\n"
        result += f"Situation: {q.get('Situation', '')}\n"
        result += f"Question: {q.get('Question', '')}\n"
        if 'Options' in q:
            result += "Options:\n"
            for i, opt in enumerate(q['Options'], 1):
                result += f"{i}. {opt}\n"
        result += "\n"
        return result

    def _create_generation_prompt(self, topic: str, context: str) -> str:
        """Create the prompt for question generation"""
        return f"""Based on these JLPT N5 listening questions, create a new question about {topic}.
        Follow this exact format and include all components.
        Use only Japanese (no English).
        Make it different from the examples but keep N5 level difficulty.
        
        {context}
        
        New Question:
        """

if __name__ == "__main__":
    try:
        print("Initializing Interactive Learning system...")
        interactive = InteractiveLearning()
        
        print("\nGenerating question about shopping...")
        new_question = interactive.generate_similar_question(3, "shopping")
        
        if new_question:
            print("\nGenerated Question:")
            print(json.dumps(new_question, indent=2, ensure_ascii=False))
        else:
            print("\nFailed to generate question")
            
    except Exception as e:
        print(f"Main execution error: {str(e)}")
        import traceback
        print("Full traceback:")
        print(traceback.format_exc())


# if __name__ == "__main__":
#     try:
#         interactive = InteractiveLearning()
        
#         # Test prompt with proper structure
#         test_prompt = """以下のフォーマットでJLPT N5レベルの買い物に関する質問を作成してください：

# Situation: [状況説明]
# Question: [質問]
# Options:
# 1. [選択肢1]
# 2. [選択肢2]
# 3. [選択肢3]
# 4. [選択肢4]"""
        
#         print("Testing Bedrock Nova invocation...")
#         response = interactive._invoke_bedrock(test_prompt)
        
#         if response:
#             print("\nReceived response:")
#             print(response)
            
#             print("\nParsing response...")
#             parsed = interactive._parse_question(response)
#             if parsed:
#                 print("\nParsed question:")
#                 print(json.dumps(parsed, indent=2, ensure_ascii=False))
#         else:
#             print("\nNo response received")
            
#     except Exception as e:
#         print(f"Error: {str(e)}")
#         import traceback
#         print(traceback.format_exc())