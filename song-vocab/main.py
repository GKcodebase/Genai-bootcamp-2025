from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from agent import SongAgent
from typing import List, Dict

app = FastAPI()

class LyricsRequest(BaseModel):
    message_request: str = Field(..., min_length=1, description="Song name and artist")
    primary_lang: str = Field(..., min_length=2, description="Primary language of the song")
    target_lang: str = Field(..., min_length=2, description="Target language for translation")

    class Config:
        schema_extra = {
            "example": {
                "message_request": "Shape of You Ed Sheeran",
                "primary_lang": "English",
                "target_lang": "Spanish"
            }
        }

class LyricsResponse(BaseModel):
    lyrics: str
    vocabulary: List[str]
    translation: Dict[str, str]

@app.post("/api/agent", response_model=LyricsResponse)
async def get_lyrics(request: LyricsRequest):
    try:
        agent = SongAgent()
        result = await agent.process(
            song_request=request.message_request,
            primary_lang=request.primary_lang,
            target_lang=request.target_lang
        )
        
        if not result:
            raise HTTPException(status_code=404, detail="Could not find lyrics for the requested song")
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))