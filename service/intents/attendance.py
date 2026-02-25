from service.metrics import get_attendance_metrics
from service.intents.types import IntentResult
from service.period_models import ResolvedPeriod
from service.intents.scope import AccessScope


def handle_attendance(scope: AccessScope, period: ResolvedPeriod) -> IntentResult:

    metrics = get_attendance_metrics(
        school_id=scope.school_id,
        student_id=scope.student_id,
        session_term_id=period.id
    )

    attendance_rate = metrics.get("attendance_rate")

    # Guardrail: No data
    if attendance_rate is None:
        return IntentResult(
            answer="Verified data is unavailable or incomplete for this request.",
            supporting_metrics={},
            data_gaps="No attendance records found for the selected period.",
            suggested_actions=["Verify attendance data source"]
        )

    # Parent-specific wording
    if scope.student_id:
        answer = (
            f"Your child's attendance rate for {period.label} "
            f"is {attendance_rate}%."
        )
    else:
        answer = (
            f"Overall attendance rate for {period.label} "
            f"is {attendance_rate}%."
        )

    return IntentResult(
        answer=answer,
        supporting_metrics=metrics,
        data_gaps=None,
        suggested_actions=[]
    )
