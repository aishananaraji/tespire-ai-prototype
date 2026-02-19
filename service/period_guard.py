from fastapi import HTTPException

def enforce_period(role: str, period: dict):
   
    if role in ["owner", "admin"]:
        return period  

    if role == "teacher":
        if period["value"] not in ["current", "recent"]:
            raise HTTPException(
                status_code=403,
                detail="Teachers can only access current or recent periods"
            )

    if role == "parent":
        if period["value"] != "current":
            raise HTTPException(
                status_code=403,
                detail="Parents can only access current period data"
            )

    return period
