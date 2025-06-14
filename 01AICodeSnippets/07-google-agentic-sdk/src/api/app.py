import os
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.agent import GoogleAgent

# Initialize FastAPI app
app = FastAPI(
    title="Google Agentic SDK API",
    description="API for Google Vertex AI Agents using Gemini",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent
agent = GoogleAgent()

# Request models
class AgentRequest(BaseModel):
    task: str
    tools: Optional[List[Dict[str, Any]]] = None
    context: Optional[str] = None

class AgentWithMemoryRequest(BaseModel):
    task: str
    conversation_history: List[Dict[str, str]]
    tools: Optional[List[Dict[str, Any]]] = None

@app.post("/agent/run")
async def run_agent(request: AgentRequest):
    """Run the agent on a task."""
    try:
        result = await agent.run_agent(
            task=request.task,
            tools=request.tools,
            context=request.context
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/agent/run-with-memory")
async def run_agent_with_memory(request: AgentWithMemoryRequest):
    """Run the agent with conversation memory."""
    try:
        result = await agent.run_agent_with_memory(
            task=request.task,
            conversation_history=request.conversation_history,
            tools=request.tools
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agent/info")
async def get_agent_info():
    """Get agent information."""
    return agent.to_dict()

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "agent": agent.to_dict()
    } 