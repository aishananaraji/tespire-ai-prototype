from service.intents.enrollment import handle_enrollment
from service.intents.attendance import handle_attendance
from service.intents.fees import handle_fees
from service.intents.performance import handle_performance
from service.intents.types import IntentResult
from service.intents.access import INTENT_ACCESS


def route_intent(intent: str, context, period) -> IntentResult:
    role = context.role

    
    allowed_roles = INTENT_ACCESS.get(intent)

    if not allowed_roles:
        return IntentResult(
            answer="I don't understand this question yet.",
            supporting_metrics={},
            data_gaps="Unknown intent",
            suggested_actions=["Try rephrasing your question"]
        )

    
    if role not in allowed_roles:
        return IntentResult(
            answer="You do not have permission to access this information.",
            supporting_metrics={},
            data_gaps="Access restricted",
            suggested_actions=[]
        )

    
    if intent == "enrollment":
        return handle_enrollment(context, period)

    if intent == "attendance":
        return handle_attendance(context, period)

    if intent == "fees":
        return handle_fees(context, period)

    if intent == "performance":
        return handle_performance(context, period)

    
    return IntentResult(
        answer="I don't understand this question yet.",
        supporting_metrics={},
        data_gaps="Unknown intent",
        suggested_actions=["Try rephrasing your question"]
    )
