from service.database import supabase

def log_ai_interaction(
    user_id: str,
    role: str,
    school_id: str,
    session_term_id: int | None,
    prompt: str,
    response: str | None,
    success: bool,
    execution_time_ms: int
):


    try:
        supabase.table("ai_logs").insert({
            "user_id": user_id,
            "role": role,
            "school_id": school_id,
            "session_term_id": session_term_id,
            "prompt": prompt,
            "response": response,
            "success": success,
            "execution_time_ms": execution_time_ms
        }).execute()

    except Exception as e:
        print("Logging failed:", str(e))
