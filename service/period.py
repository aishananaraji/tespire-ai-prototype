from datetime import datetime
def resolve_period(requested_period: str | None):
    """
    Resolves the correct academic period.
    """
    if requested_period:
        return requested_period
    
    current_year = datetime.now().year
    return f"{current_year}_TERM 1" 