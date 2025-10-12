"""
Analytics calculators for EmpathZ AI Coordinator Demo
Handles computation of call statistics and risk distributions
"""

from typing import List, Dict, Any

def compute_analytics(visible_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compute analytics for visible calls
    Returns dictionary with total calls, risk distribution, and average response time
    """
    if not visible_calls:
        return {
            "total_calls": 0,
            "risk_distribution": {i: 0 for i in range(6)},
            "avg_response_time": 0
        }
    
    risk_distribution = calculate_risk_distribution(visible_calls)
    avg_response_time = calculate_avg_response_time(visible_calls)
    
    return {
        "total_calls": len(visible_calls),
        "risk_distribution": risk_distribution,
        "avg_response_time": avg_response_time
    }

def calculate_risk_distribution(calls: List[Dict[str, Any]]) -> Dict[int, int]:
    """
    Calculate risk level distribution based on highest risk dimension per call
    Returns dictionary mapping risk level (0-5) to count of calls
    """
    distribution = {i: 0 for i in range(6)}
    
    for call in calls:
        risk = call.get("risk", {})
        max_risk = 0
        
        # Find the highest risk score across all dimensions
        for dimension in ["suicide", "homicide", "self_harm", "harm_others"]:
            if dimension in risk:
                score = risk[dimension].get("score", 0)
                max_risk = max(max_risk, score)
        
        distribution[max_risk] += 1
    
    return distribution

def calculate_avg_response_time(calls: List[Dict[str, Any]]) -> float:
    """
    Calculate average response time from analytics.response_time_sec
    Returns average in seconds
    """
    if not calls:
        return 0.0
    
    total_time = 0
    valid_calls = 0
    
    for call in calls:
        analytics = call.get("analytics", {})
        response_time = analytics.get("response_time_sec", 0)
        
        if response_time > 0:
            total_time += response_time
            valid_calls += 1
    
    return total_time / valid_calls if valid_calls > 0 else 0.0

def get_risk_summary(calls: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Get summary of risk levels across all calls
    Returns counts for high (4-5), moderate (2-3), and low (0-1) risk
    """
    distribution = calculate_risk_distribution(calls)
    
    high_risk = distribution.get(4, 0) + distribution.get(5, 0)
    moderate_risk = distribution.get(2, 0) + distribution.get(3, 0)
    low_risk = distribution.get(0, 0) + distribution.get(1, 0)
    
    return {
        "high_risk": high_risk,
        "moderate_risk": moderate_risk,
        "low_risk": low_risk,
        "total": sum(distribution.values())
    }

def get_call_statistics(calls: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Get comprehensive call statistics
    Returns dictionary with various metrics
    """
    if not calls:
        return {
            "total_calls": 0,
            "total_duration_minutes": 0,
            "avg_duration_minutes": 0,
            "channels": {},
            "languages": {},
            "age_ranges": {}
        }
    
    total_duration = 0
    channels = {}
    languages = {}
    age_ranges = {}
    
    for call in calls:
        # Duration
        duration_sec = call.get("duration_sec", 0)
        total_duration += duration_sec
        
        # Channel distribution
        channel = call.get("channel", "unknown")
        channels[channel] = channels.get(channel, 0) + 1
        
        # Language distribution
        language = call.get("language", "unknown")
        languages[language] = languages.get(language, 0) + 1
        
        # Age range distribution
        age_range = call.get("caller_profile", {}).get("age_range", "unknown")
        age_ranges[age_range] = age_ranges.get(age_range, 0) + 1
    
    return {
        "total_calls": len(calls),
        "total_duration_minutes": total_duration / 60,
        "avg_duration_minutes": (total_duration / len(calls)) / 60,
        "channels": channels,
        "languages": languages,
        "age_ranges": age_ranges
    }
