from datetime import datetime
from typing import Dict, List, Optional
from main import AskResponse  

def build_response(
    *,
    answer: str,
    supporting_metrics: Dict,
    role: str,
    period: str,
    school_id: str,
    data_gaps: Optional[str] = None,
    suggested_actions: Optional[List[str]] = None,
):
    return AskResponse(
        answer=answer,
        supporting_metrics=supporting_metrics,
        data_gaps=data_gaps,
        suggested_actions=suggested_actions or [],
        data_scope_used={
            "period": period,
            "school_id": school_id,
            "role": role,
        },
        timestamp=datetime.utcnow(),
    )
