from typing import Dict, Union, Optional, List
from datetime import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from service.reasoning import classify_intent
from service.metrics import (
    get_enrollment_metrics,
    get_attendance_metrics,
    get_fee_metrics,
    get_performance_metrics,
)

# ------------------------
# APP
# ------------------------

app = FastAPI(title="Tespire AI Prototype")

# ------------------------
# INPUT CONTRACT (PRD)
# ------------------------

class AskContext(BaseModel):
    role: str  # owner, admin, teacher, parent
    school_id: str


class AskRequest(BaseModel):
    question: str
    period: Optional[str] = None
    context: AskContext


# ------------------------
# OUTPUT CONTRACT (PRD)
# ------------------------

class AskResponse(BaseModel):
    answer: str
    supporting_metrics: Dict[str, Union[int, float]]
    data_gaps: Optional[str]
    suggested_actions: List[str]
    data_scope_used: Dict[str, str]
    timestamp: datetime


# ------------------------
# GUARDRAILS (RBAC)
# ------------------------

ALLOWED_ROLES = ["owner", "admin", "teacher", "parent"]

def role_guard(role: str):
    role = role.lower()
    if role not in ALLOWED_ROLES:
        raise HTTPException(
            status_code=403,
            detail="Invalid role"
        )
    return role


# ------------------------
# HEALTH CHECK
# ------------------------

@app.get("/")
def root():
    return {"message": "Tespire AI backend is running"}


# ------------------------
# AI ENDPOINT
# ------------------------

@app.post("/ask", response_model=AskResponse)
def ask_tespire_ai(payload: AskRequest):
    
    role = role_guard(payload.context.role)
    intent = classify_intent(payload.question)

    # Route to correct metric
    if intent == "enrollment":
        metrics = get_enrollment_metrics(payload.context.school_id)

    elif intent == "attendance":
        metrics = get_attendance_metrics(payload.context.school_id)

    elif intent == "fees":
        metrics = get_fee_metrics(payload.context.school_id)

    elif intent == "performance":
        metrics = get_performance_metrics(payload.context.school_id)

    else:
        return AskResponse(
            answer="I don't understand this question yet.",
            supporting_metrics={},
            data_gaps="Unknown intent",
            suggested_actions=["Rephrase your question"],
            data_scope_used={
                "period": payload.period or "Current Term",
                "school_id": payload.context.school_id,
                "role": role,
            },
            timestamp=datetime.utcnow()
        )

    # ------------------------
    # SAFETY CHECK (DATA GAP)
    # ------------------------

    if not metrics or metrics.get("total_students", 1) == 0:
        return AskResponse(
            answer="No student data available for this school.",
            supporting_metrics={},
            data_gaps="No student records found",
            suggested_actions=["Verify school data source"],
            data_scope_used={
                "period": payload.period or "Current Term",
                "school_id": payload.context.school_id,
                "role": role,
            },
            timestamp=datetime.utcnow()
        )

    # ------------------------
    # ROLE-BASED RESPONSE
    # ------------------------

    if role == "parent":
        supporting_metrics = {
            "active_students": metrics.get("active_students", 0)
        }
        answer = "Your child is currently active in school."

    else:
        supporting_metrics = metrics
        answer = f"{intent.capitalize()} rate is {metrics.get(f'{intent}_rate', 'N/A')}"

    return AskResponse(
        answer=answer,
        supporting_metrics=supporting_metrics,
        data_gaps=None,
        suggested_actions=[
            "Review pending enrollments",
            "Notify admissions office"
        ],
        data_scope_used={
            "period": payload.period or "Current Term",
            "school_id": payload.context.school_id,
            "role": role,
        },
        timestamp=datetime.utcnow()
    )