from service.metrics import get_payment_metrics
from service.intents.types import IntentResult
from service.period_models import ResolvedPeriod
from service.intents.scope import AccessScope


def handle_fees(scope: AccessScope, period: ResolvedPeriod) -> IntentResult:

    metrics = get_payment_metrics(
        school_id=scope.school_id,
        student_id=scope.student_id,
        session_term_id=period.id
    )

    total_due = metrics.get("total_due")
    total_paid = metrics.get("total_paid")
    outstanding = metrics.get("outstanding")

    if total_due is None:
        return IntentResult(
            answer="Verified data is unavailable or incomplete for this request.",
            supporting_metrics={},
            data_gaps="No fee records found for the selected period.",
            suggested_actions=["Verify fee data source"]
        )

    if scope.student_id:
        answer = (
            f"Your child's total fees for {period.label} are {total_due}, "
            f"with {total_paid} paid and {outstanding} outstanding."
        )
    else:
        answer = (
            f"Total school fees for {period.label} are {total_due}, "
            f"with {total_paid} collected and {outstanding} outstanding."
        )

    return IntentResult(
        answer=answer,
        supporting_metrics=metrics,
        data_gaps=None,
        suggested_actions=[]
    )
