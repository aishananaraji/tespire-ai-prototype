from service.metrics import get_enrollment_metrics
from service.intents.types import IntentResult
from service.intents.scope import AccessScope


def handle_enrollment(scope: AccessScope, period: dict) -> IntentResult:

    metrics = get_enrollment_metrics(
        school_id=scope.school_id,
        student_id=scope.student_id,
        session_term_id=period["id"]
    )

    total_students = metrics.get("total_students")

    if total_students is None:
        return IntentResult(
            answer="Verified data is unavailable or incomplete for this request.",
            supporting_metrics={},
            data_gaps="No enrollment records found for the selected period.",
            suggested_actions=["Verify school data source"]
        )

    enrollment_rate = metrics.get("enrollment_rate", "N/A")

    if scope.student_id:
        answer = f"Your child is enrolled for this academic period."
    else:
        answer = f"Total enrolled students this period: {total_students}."

    return IntentResult(
        answer=answer,
        supporting_metrics=metrics,
        data_gaps=None,
        suggested_actions=[]
    )

