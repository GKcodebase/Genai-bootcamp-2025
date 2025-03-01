from youtube_transcript_api import YouTubeTranscriptApi
from typing import Optional, List, Dict
import os


class YouTubeTranscriptDownloader:
    def __init__(self, languages: List[str] = ["ja", "en"]):
        self.languages = languages

    def extract_video_id(self, url: str) -> Optional[str]:
        """
        Extract video ID from YouTube URL
        
        Args:
            url (str): YouTube URL
            
        Returns:
            Optional[str]: Video ID if found, None otherwise
        """
        if "v=" in url:
            return url.split("v=")[1][:11]
        elif "youtu.be/" in url:
            return url.split("youtu.be/")[1][:11]
        return None

    def get_transcript(self, video_id: str) -> Optional[List[Dict]]:
        """
        Download YouTube Transcript
        
        Args:
            video_id (str): YouTube video ID or URL
            
        Returns:
            Optional[List[Dict]]: Transcript if successful, None otherwise
        """
        # Extract video ID if full URL is provided
        if "youtube.com" in video_id or "youtu.be" in video_id:
            video_id = self.extract_video_id(video_id)
            
        if not video_id:
            print("Invalid video ID or URL")
            return None

        print(f"Downloading transcript for video ID: {video_id}")
        
        try:
            return YouTubeTranscriptApi.get_transcript(video_id, languages=self.languages)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

    def save_transcript(self, transcript: List[Dict], video_id: str) -> bool:
        """
        Save transcript to file
        
        Args:
            transcript (List[Dict]): Transcript data
            video_id (str): YouTube video ID for filename
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create data/transcripts directory if it doesn't exist
            os.makedirs("../backend/data/transcripts", exist_ok=True)
            
            # Full path for transcript file
            filename = f"../backend/data/transcripts/{video_id}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                for entry in transcript:
                    f.write(f"{entry['text']}\n")
            return True
        except Exception as e:
            print(f"Error saving transcript: {str(e)}")
            return False

def main(video_url: str, print_transcript: bool = False) -> Optional[str]:
    """
    Main function to download and save transcript
    
    Args:
        video_url (str): YouTube video URL
        print_transcript (bool): Whether to print the transcript
        
    Returns:
        Optional[str]: Video ID if successful, None otherwise
    """
    # Initialize downloader
    downloader = YouTubeTranscriptDownloader()
    
    # Extract video ID
    video_id = downloader.extract_video_id(video_url)
    if not video_id:
        print("Failed to extract video ID")
        return None
    
    # Get transcript
    transcript = downloader.get_transcript(video_id)
    
    if transcript:
        if downloader.save_transcript(transcript, video_id):
            print(f"Transcript saved successfully to data/transcripts/{video_id}.txt")
            if print_transcript:
                for entry in transcript:
                    print(f"{entry['text']}")
            return video_id
        else:
            print("Failed to save transcript")
    else:
        print("Failed to get transcript")
    
    return None

if __name__ == "__main__":
    video_id = "https://www.youtube.com/watch?v=sY7L5cfCWno&list=PLkGU7DnOLgRMl-h4NxxrGbK-UdZHIXzKQ"  # Extract from URL: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    transcript = main(video_id, print_transcript=True)
