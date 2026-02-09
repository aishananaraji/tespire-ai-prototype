from service.metrics import get_performance_metrics
from service.intents.types import IntentResult


def handle_performance(context, period) -> IntentResult:
    metrics = get_performance_metrics(
        school_id=context.school_id,
        period=period
    )

    average_score = metrics.get("average_score")

    
    if average_score is None:
        return IntentResult(
            answer="Verified data is unavailable or incomplete for this request.",
            supporting_metrics={},
            data_gaps="No academic performance records found.",
            suggested_actions=["Verify academic records"]
        )

    return IntentResult(
        answer=f"Average academic score for the selected period is {average_score}.",
        supporting_metrics=metrics,
        data_gaps=None,
        suggested_actions=[
            "Review low-performing subjects",
            "Support struggling students"
        ]
    )
