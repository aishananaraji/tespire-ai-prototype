from typing import Dict, List, Optional
from pydantic import BaseModel


class IntentResult(BaseModel):
    answer: str
    supporting_metrics: Dict
    data_gaps: Optional[str] = None
    suggested_actions: Optional[List[str]] = None
