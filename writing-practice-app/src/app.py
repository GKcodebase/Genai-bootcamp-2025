import gradio as gr
import requests
from manga_ocr import MangaOcr
from typing import Dict, List
import os
import random
import logging
from enum import Enum
import groq
import yaml
import dotenv

dotenv.load_dotenv()

# Setup Custom Logging
logger = logging.getLogger('japanese_app')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('app.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.propagate = False

class AppState(Enum):
    SETUP = "setup"
    PRACTICE = "practice"
    REVIEW = "review"

class JapaneseLearningApp:
    def __init__(self):
        self.mocr = MangaOcr()
        self.vocabulary = None
        self.current_state = AppState.SETUP
        self.current_sentence = ""
        # Initialize Groq client instead of OpenAI
        self.client = groq.Groq(api_key=os.getenv('GROQ_API_KEY'))
        self.study_session_id = os.getenv('SESSION_ID', '1')
        self.load_vocabulary()

    def load_vocabulary(self, group_id: int = 1):
        """Fetch vocabulary from API"""
        try:
            url = f'http://localhost:5000/api/groups/{group_id}/words/raw'
            logger.debug(f"Fetching vocabulary from: {url}")
            
            response = requests.get(url)
            if response.status_code == 200:
                self.vocabulary = response.json()
                logger.info(f"Loaded {len(self.vocabulary.get('words', []))} words")
            else:
                logger.error(f"API request failed: {response.status_code}")
                self.vocabulary = None
        except Exception as e:
            logger.error(f"Failed to load vocabulary: {e}")
            self.vocabulary = None

    def generate_sentence(self, word: dict) -> str:
        """Generate a sentence using Groq API"""
        kanji = word.get('kanji', '')
        prompt = f"""Generate a simple Japanese sentence using the word '{kanji}'.
        The grammar should be scoped to JLPTN5 grammar.
        Please provide the response in this format:
        Japanese: [sentence in kanji/hiragana]
        English: [English translation]
        """
        
        logger.debug(f"Generating sentence for word: {kanji}")
        response = self.client.chat.completions.create(
            model="mixtral-8x7b-32768",  # Groq's model
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=100
        )
        return response.choices[0].message.content.strip()

    def grade_submission(self, image_path: str) -> Dict:
        """Process image submission and grade it"""
        try:
            # Get transcription from image
            transcription = self.mocr(image_path)
            logger.debug(f"Transcription result: {transcription}")
            
            # Get literal translation using Groq
            translation_prompt = f"""
            Translate and evaluate this Japanese text: {transcription}
            Compare it with the original sentence: {self.current_sentence}
            
            Please analyze:
            1. Character accuracy (proper stroke order and formation)
            2. Whether the meaning matches the original sentence
            3. Grammar correctness
            
            Provide response in this format:
            Translation: [English translation]
            Accuracy: [percentage 0-100]
            Grade: [S/A/B/C/D based on accuracy: S>90, A>80, B>70, C>60, D<60]
            Feedback: [Specific feedback about writing, translation and grammar]
            """
            
            evaluation_response = self.client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": translation_prompt}],
                temperature=0.3,
                max_tokens=200
            )
            
            # Parse the response
            response_text = evaluation_response.choices[0].message.content.strip()
            evaluation_lines = response_text.split('\n')
            
            # Extract evaluation components
            translation = ""
            accuracy = 0
            grade = "C"
            feedback = ""
            
            for line in evaluation_lines:
                if line.startswith("Translation:"):
                    translation = line.replace("Translation:", "").strip()
                elif line.startswith("Accuracy:"):
                    accuracy = int(line.replace("Accuracy:", "").replace("%", "").strip())
                    grade = "S" if accuracy > 90 else "A" if accuracy > 80 else "B" if accuracy > 70 else "C" if accuracy > 60 else "D"
                elif line.startswith("Feedback:"):
                    feedback = line.replace("Feedback:", "").strip()
            
            return {
                "transcription": transcription,
                "translation": translation,
                "grade": grade,
                "accuracy": f"{accuracy}%",
                "feedback": feedback
            }
        except Exception as e:
            logger.error(f"Error in grade_submission: {str(e)}")
            return {
                "transcription": "Error processing submission",
                "translation": "Error",
                "grade": "C",
                "accuracy": "0%",
                "feedback": f"An error occurred: {str(e)}"
            }

def create_ui(app_instance: JapaneseLearningApp):
    custom_css = """
    .large-text-output textarea {
        font-size: 40px !important;
        line-height: 1.5 !important;
        font-family: 'Noto Sans JP', sans-serif !important;
    }
    """
    
    with gr.Blocks(title="Japanese Writing Practice", css=custom_css) as ui:
        state = gr.State(value=AppState.SETUP.value)
        current_sentence = gr.State(value="")

        with gr.Group(visible=True) as setup_group:
            gr.Markdown("# Japanese Writing Practice")
            generate_btn = gr.Button("Generate Sentence", variant="primary")

        with gr.Group(visible=False) as practice_group:
            sentence_display = gr.Markdown(elem_classes=["large-text-output"])
            image_upload = gr.Image(type="filepath", label="Upload your writing")
            submit_btn = gr.Button("Submit for Review", variant="secondary")

        with gr.Group(visible=False) as review_group:
            review_sentence = gr.Markdown(elem_classes=["large-text-output"])
            transcription = gr.Markdown()
            translation = gr.Markdown()
            feedback = gr.Markdown()
            next_btn = gr.Button("Next Question", variant="primary")

        def switch_to_practice(_state):
            if not app_instance.vocabulary:
                return [
                    gr.update(visible=True),   # setup_group
                    gr.update(visible=False),  # practice_group
                    gr.update(visible=False),  # review_group
                    "Error: No vocabulary loaded",  # sentence_display
                    AppState.SETUP.value  # state
                ]

            word = random.choice(app_instance.vocabulary['words'])
            new_sentence = app_instance.generate_sentence(word)
            app_instance.current_sentence = new_sentence

            return [
                gr.update(visible=False),  # setup_group
                gr.update(visible=True),   # practice_group
                gr.update(visible=False),  # review_group
                new_sentence,              # sentence_display
                AppState.PRACTICE.value    # state
            ]

        def switch_to_review(image, _state, _current_sent):
            if not image:
                return None
                
            review_data = app_instance.grade_submission(image)
            
            # Create detailed feedback message
            feedback_message = f"""
            Grade: {review_data['grade']} ({review_data['accuracy']})
            
            Transcription: {review_data['transcription']}
            Translation: {review_data['translation']}
            
            Feedback: {review_data['feedback']}
            """
            
            return [
                gr.update(visible=False),  # setup_group
                gr.update(visible=False),  # practice_group
                gr.update(visible=True),   # review_group
                app_instance.current_sentence,  # review_sentence
                f"Transcription: {review_data['transcription']}",  # transcription
                f"Translation: {review_data['translation']}",  # translation
                feedback_message,  # feedback
                AppState.REVIEW.value  # state
            ]

        generate_btn.click(
            fn=switch_to_practice,
            inputs=[state],
            outputs=[
                setup_group,
                practice_group,
                review_group,
                sentence_display,
                state
            ]
        )

        submit_btn.click(
            fn=switch_to_review,
            inputs=[image_upload, state, current_sentence],
            outputs=[
                setup_group,
                practice_group,
                review_group,
                review_sentence,
                transcription,
                translation,
                feedback,
                state
            ]
        )

        next_btn.click(
            fn=switch_to_practice,
            inputs=[state],
            outputs=[
                setup_group,
                practice_group,
                review_group,
                sentence_display,
                state
            ]
        )

    return ui

if __name__ == "__main__":
    app_instance = JapaneseLearningApp()
    ui = create_ui(app_instance)
    ui.launch(server_name="127.0.0.1", server_port=7860)  # Remove share=True