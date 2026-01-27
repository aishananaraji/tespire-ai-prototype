from supabase import create_client
from dotenv import load_dotenv
import os

USE_MOCK_DATA = True

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

#-------- Enrollment ------------------

def get_enrollment_metrics(school_id: str):
    if USE_MOCK_DATA:
        return{
            "total_students": 120,
            "active_students": 95,
            "enrollment_rate": 0.79
        }
    students = supabase.table("students")\

    data = students.data

    # Step 1: Safety check FIRST
    if not data:
        return {
            "total_students": 0,
            "active_students": 0,
            "enrollment_rate": 0
        }

    # Step 2: Normal logic
    total_students = len(data)
    active_students = len([
        s for s in data if s["status"] == "enrolled"
    ])

    enrollment_rate = (
        active_students / total_students
        if total_students > 0 else 0
    )

    # Step 3: Final return
    return {
        "total_students": total_students,
        "active_students": active_students,
        "enrollment_rate": round(enrollment_rate, 2)
    }

# -------- Attendance --------
def get_attendance_metrics(school_id: str):
    if USE_MOCK_DATA:
        return {"attendance_rate": 0.88}

    records = supabase.table("attendance") \
        .eq("school_id", school_id) \
        .execute()

    data = records.data

    if not data:
        return {"attendance_rate": 0}

    present_count = len([r for r in data if r["present"] is True])
    attendance_rate = present_count / len(data)

    return {
        "attendance_rate": round(attendance_rate, 2)
    }


# -------- Fees --------
def get_fee_metrics(school_id: str):
    if USE_MOCK_DATA:
       return {
          "total_revenue": 500000,
          "outstanding": 120000
       }
    records = supabase.table("fees").execute()

    data = records.data

    if not data:
        return {"total_revenue": 0, "outstanding": 0}

    total = sum([r["amount"] for r in data])
    paid = sum([r["amount"] for r in data if r["paid"] is True])
    outstanding = total - paid

    return {
        "total_revenue": total,
        "outstanding": outstanding
    }


# -------- Performance --------
def get_performance_metrics(school_id: str):
    if USE_MOCK_DATA:
        return {"average_score": 63.5}

    records = supabase.table("results") \
        .eq("school_id", school_id) \
        .execute()

    data = records.data

    if not data:
        return {"average_score": 0}

    avg = sum(r["score"] for r in data) / len(data)

    return {
        "average_score": round(avg, 2)
    }
