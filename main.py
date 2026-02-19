from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from service.llm import llm_reason
from service.period import resolve_period
from service.memory import get_history, save_turn
from service.intent_router import route_intent
from service.response_builder import build_response
from service.period_guard import enforce_period
import time
from service.logging_hook import log_ai_interaction



app = FastAPI(title="Tespire AI Prototype")


# INPUT CONTRACT

class AskContext(BaseModel):
    role: str
    school_id: str
    session_id: str
    student_id: Optional[str] = None


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



@app.get("/")
def root():
    return {"message": "Tespire AI backend is running"}


# AI ENDPOINT

@app.post("/ask")
def ask_tespire_ai(payload: AskRequest):

    start_time = time.time()
    success = True
    response_text = None

    try:
       
        role = role_guard(payload.context.role)
        resolved_period = resolve_period(
            school_id=payload.context.school_id,
            requested_session_term_id=payload.period
            )

        if role == "parent" and not payload.context.student_id:
            raise HTTPException(
                status_code=400,
                detail="Parent requests must include student_id"
            )

       
        history = get_history(payload.context.session_id)

        ai_decision = llm_reason(
            payload.question,
            context=payload.context.dict(),
            history=history
        )

        intent = ai_decision.get("intent")

    
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

        final_response = build_response(
            answer=result.answer,
            supporting_metrics=result.supporting_metrics,
            data_gaps=result.data_gaps,
            suggested_actions=result.suggested_actions,
            role=role,
            period=resolved_period,
            school_id=payload.context.school_id,
        )

        response_text = final_response["answer"]

        return final_response

    except Exception as e:
        success = False
        response_text = str(e)
        raise e

    finally:
        execution_time_ms = int((time.time() - start_time) * 1000)

        log_ai_interaction(
            user_id=getattr(payload.context, "user_id", payload.context.session_id),
            role=role if "role" in locals() else payload.context.role,
            school_id=payload.context.school_id,
            session_term_id=(
                resolved_period.get("id")
                if "resolved_period" in locals() and isinstance(resolved_period, dict)
                else None
            ),
            prompt=payload.question,
            response=response_text,
            success=success,
            execution_time_ms=execution_time_ms
        )
