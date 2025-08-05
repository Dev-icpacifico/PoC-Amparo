from fastapi import FastAPI
from pydantic import BaseModel
from app.agent_runner import run_agent

app = FastAPI()

class ChatRequest(BaseModel):
    user_id: str
    message: str
    session_id: str = None

@app.post("/chat/")
async def chat(payload: ChatRequest):
    response = run_agent(payload.user_id, payload.message, payload.session_id)
    return {"respuesta": response}
