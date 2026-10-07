from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# In-memory database store
calls_db: Dict[str, dict] = {}

class CallEndedPayload(BaseModel):
    call_id: str
    status: str
    duration_secs: int

@app.post("/call-ended", status_code=status.HTTP_200_OK)
def receive_call_ended(payload: CallEndedPayload):
    if not payload.call_id or not payload.call_id.strip():
        raise HTTPException(status_code=400, detail="call_id must not be empty")
    
    # Idempotent storage: do not duplicate record if call_id already exists
    if payload.call_id not in calls_db:
        calls_db[payload.call_id] = payload.model_dump()
        
    return {"status": "success", "call_id": payload.call_id}

@app.get("/calls/{call_id}")
def get_call_record(call_id: str):
    if call_id not in calls_db:
        raise HTTPException(status_code=404, detail="Call record not found")
    return calls_db[call_id]
