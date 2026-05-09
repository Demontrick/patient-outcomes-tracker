from typing import List, Dict
from datetime import datetime

def calculate_trend(scores: List[Dict[str, any]]) -> str:
    """
    Calculate trend based on score delta.
    Expects scores sorted by timestamp ascending.
    """
    if len(scores) < 2:
        return "Stable"
    
    # Simple logic: compare average of last 2 with average of previous 2 (if available)
    # or just compare last with first in the window.
    # For this app, we'll use the delta between the most recent and the previous reading.
    
    latest = scores[-1]["score"]
    previous = scores[-2]["score"]
    
    delta = latest - previous
    
    if delta > 5:
        return "Improving"
    elif delta < -5:
        return "Deteriorating"
    else:
        return "Stable"

def get_patient_trend_data(outcomes: List) -> Dict:
    """
    Process outcomes to return trend status and score history.
    """
    sorted_outcomes = sorted(
        [{"score": o.score, "timestamp": o.timestamp} for o in outcomes],
        key=lambda x: x["timestamp"]
    )
    
    trend = calculate_trend(sorted_outcomes)
    
    return {
        "trend": trend,
        "history": sorted_outcomes,
        "current_score": sorted_outcomes[-1]["score"] if sorted_outcomes else None
    }
