from dataclasses import dataclass
from typing import Optional

@dataclass
class AccessScope:
    school_id: str
    student_id: Optional[str]
