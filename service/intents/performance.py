from service.metrics import get_performance_metrics
from service.intents.types import IntentResult
from service.period_models import ResolvedPeriod
from service.intents.scope import AccessScope


def handle_performance(scope: AccessScope, period: ResolvedPeriod) -> IntentResult:

    metrics = get_performance_metrics(
        school_id=scope.school_id,
        student_id=scope.student_id,
        session_term_id=period.id
    )

    average_score = metrics.get("average_score")

    if average_score is None:
        return IntentResult(
            answer="Verified data is unavailable or incomplete for this request.",
            supporting_metrics={},
            data_gaps="No performance records found for the selected period.",
            suggested_actions=["Verify academic performance data source"]
        )

    if scope.student_id:
        answer = (
            f"Your child's average performance score for {period.label} "
            f"is {average_score}."
        )
    else:
        answer = (
            f"The overall average performance score for {period.label} "
            f"is {average_score}."
        )

    return IntentResult(
        answer=answer,
        supporting_metrics=metrics,
        data_gaps=None,
        suggested_actions=[]
    )
