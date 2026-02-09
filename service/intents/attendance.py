from service.metrics import get_attendance_metrics
from service.intents.types import IntentResult


def handle_attendance(context, period) -> IntentResult:
    metrics = get_attendance_metrics(
        school_id=context.school_id,
        period=period
    )

    attendance_rate = metrics.get("attendance_rate")

    
    if attendance_rate is None:
        return IntentResult(
            answer="Verified data is unavailable or incomplete for this request.",
            supporting_metrics={},
            data_gaps="No attendance records found for the selected period.",
            suggested_actions=["Verify attendance data source"]
        )

    return IntentResult(
        answer=f"Attendance rate for the selected period is {attendance_rate}%.",
        supporting_metrics=metrics,
        data_gaps=None,
        suggested_actions=[
            "Review absentee trends",
            "Follow up on frequently absent students"
        ]
    )
