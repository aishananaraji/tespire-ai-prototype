from service.metrics import get_fee_metrics
from service.intents.types import IntentResult


def handle_fees(context, period) -> IntentResult:
    metrics = get_fee_metrics(
        school_id=context.school_id,
        period=period
    )

    outstanding = metrics.get("outstanding_fees")

    
    if outstanding is None:
        return IntentResult(
            answer="Verified data is unavailable or incomplete for this request.",
            supporting_metrics={},
            data_gaps="No fee records found for the selected period.",
            suggested_actions=["Verify fee records"]
        )

    return IntentResult(
        answer=f"Outstanding fees for the selected period are {outstanding}.",
        supporting_metrics=metrics,
        data_gaps=None,
        suggested_actions=[
            "Review unpaid balances",
            "Follow up with guardians"
        ]
    )
