from supabase import create_client
from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def resolve_period(school_id: str, requested_session_term_id: int | None = None) -> int:

    
    if requested_session_term_id:
        record = (
            supabase.table("session_terms")
            .eq("id", requested_session_term_id)
            .eq("school_id", school_id)
            .limit(1)
            .execute()
        )

        if not record.data:
            raise Exception("Invalid academic period for this school.")

        return record.data[0]["id"]

    
    record = (
        supabase.table("session_terms")
        .eq("school_id", school_id)
        .eq("is_current", True)
        .limit(1)
        .execute()
    )

    if not record.data:
        raise Exception("No active academic period configured.")

    return record.data[0]["id"]

