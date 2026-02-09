from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from service.llm import llm_reason
from service.period import resolve_period
from service.memory import get_history, save_turn
from service.intent_router import route_intent
from service.response_builder import build_response


app = FastAPI(title="Tespire AI Prototype")


# INPUT CONTRACT

class AskContext(BaseModel):
    role: str
    school_id: str
    session_id: str


class AskRequest(BaseModel):
    question: str
    period: Optional[str] = None
    context: AskContext



# GUARDRAILS 

ALLOWED_ROLES = ["owner", "admin", "teacher", "parent"]


def role_guard(role: str) -> str:
    role = role.lower()
    if role not in ALLOWED_ROLES:
        raise HTTPException(
            status_code=403,
            detail="Invalid role"
        )
    return role



# HEALTH CHECK
@app.get("/")
def root():
    return {"message": "Tespire AI backend is running"}


# AI ENDPOINT

@app.post("/ask")
def ask_tespire_ai(payload: AskRequest):
    
    role = role_guard(payload.context.role)
    resolved_period = resolve_period(payload.period)

    
    history = get_history(payload.context.session_id)

    
    ai_decision = llm_reason(
        payload.question,
        context=payload.context.dict(),
        history=history
    )

    intent = ai_decision.get("intent")

    
    if role == "parent" and intent in ["fees", "performance"]:
        return build_response(
            answer="You do not have permission to access this information.",
            supporting_metrics={},
            data_gaps=None,
            suggested_actions=[],
            role=role,
            period=resolved_period,
            school_id=payload.context.school_id,
        )


    
    result = route_intent(
        intent=intent,
        context=payload.context,
        period=resolved_period
    )

    
    save_turn(
        payload.context.session_id,
        payload.question,
        result.answer
    )

    
    return build_response(
        answer=result.answer,
        supporting_metrics=result.supporting_metrics,
        data_gaps=result.data_gaps,
        suggested_actions=result.suggested_actions,
        role=role,
        period=resolved_period,
        school_id=payload.context.school_id,
    )

