from fastapi import HTTPException
from service.database import supabase
from service.period_models import ResolvedPeriod


def resolve_period(
    school_id: str,
    requested_session_term_id: int | None = None
) -> ResolvedPeriod:

    if requested_session_term_id:

        record = (
            supabase.table("session_terms")
            .eq("id", requested_session_term_id)
            .eq("school_id", school_id)
            .limit(1)
            .execute()
        )

        if not record.data:
            raise HTTPException(
                status_code=400,
                detail="Invalid academic period for this school."
            )

        period_data = record.data[0]

        return ResolvedPeriod(
            id=period_data["id"],
            label=period_data.get("name", "Academic Term"),
            value="historical",
            type="term"
        )

    record = (
        supabase.table("session_terms")
        .eq("school_id", school_id)
        .eq("is_current", True)
        .limit(1)
        .execute()
    )

    if not record.data:
        raise HTTPException(
            status_code=400,
            detail="No active academic period configured."
        )

    period_data = record.data[0]

    return ResolvedPeriod(
        id=period_data["id"],
        label=period_data.get("name", "Current Term"),
        value="current",
        type="term"
    )