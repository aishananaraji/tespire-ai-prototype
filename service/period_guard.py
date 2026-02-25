from fastapi import HTTPException
from service.period_models import ResolvedPeriod


def enforce_period(role: str, period: ResolvedPeriod) -> ResolvedPeriod:

    # Owners and admins can access any period
    if role in ["owner", "admin"]:
        return period

    # Teachers: only current or recent
    if role == "teacher":
        if period.value not in ["current", "recent"]:
            raise HTTPException(
                status_code=403,
                detail="Teachers can only access current or recent periods"
            )

    # Parents: only current
    if role == "parent":
        if period.value != "current":
            raise HTTPException(
                status_code=403,
                detail="Parents can only access current period data"
            )

    return period
