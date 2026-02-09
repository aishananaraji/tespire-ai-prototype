from service.metrics import get_enrollment_metrics
from service.intents.types import IntentResult


def handle_enrollment(context, period) -> IntentResult:
    metrics = get_enrollment_metrics(context.school_id)

    total_students = metrics.get("total_students", 0)

    
    if total_students is None:
        return IntentResult(
            answer="Verified data is unavailable or incomplete for this request.",
            supporting_metrics={},
            data_gaps="No enrollment records found",
            suggested_actions=["Verify school data source"]
        )

    enrollment_rate = metrics.get("enrollment_rate", "N/A")

    return IntentResult(
        answer=f"Enrollment rate is {enrollment_rate}",
        supporting_metrics=metrics,
        data_gaps=None,
        suggested_actions=[
            "Review pending enrollments",
            "Follow up on incomplete registrations"
        ]
    )
