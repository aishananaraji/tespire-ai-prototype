from datetime import datetime
from typing import Dict, List, Optional
from service.period_models import ResolvedPeriod
from main import AskResponse  


def build_response(
    *,
    answer: str,
    supporting_metrics: Dict,
    role: str,
    period: ResolvedPeriod,
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
            "school_id": school_id,
            "role": role,
            "period_id": period.id,
            "period_label": period.label,
            "period_type": period.type,
        },
        timestamp=datetime.utcnow(),
    )
