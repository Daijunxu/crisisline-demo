"""
Risk assessment rules for EmpathZ AI Coordinator Demo
Handles determination of RED alerts and risk level validations
"""

from typing import Dict, Any, List

def has_red_alert(risk_obj: Dict[str, Any]) -> bool:
    """
    Check if any risk dimension has a score >= 4 (RED alert threshold)
    Returns True if RED alert should be triggered
    """
    risk_dimensions = ["suicide", "homicide", "self_harm", "harm_others"]
    
    for dimension in risk_dimensions:
        if dimension in risk_obj:
            score = risk_obj[dimension].get("score", 0)
            if score >= 4:
                return True
    
    return False

def get_highest_risk_score(risk_obj: Dict[str, Any]) -> int:
    """
    Get the highest risk score across all dimensions
    Returns the maximum score (0-5)
    """
    max_score = 0
    risk_dimensions = ["suicide", "homicide", "self_harm", "harm_others"]
    
    for dimension in risk_dimensions:
        if dimension in risk_obj:
            score = risk_obj[dimension].get("score", 0)
            max_score = max(max_score, score)
    
    return max_score

def get_risk_level_description(score: int) -> str:
    """
    Get human-readable description of risk level
    Returns description string
    """
    if score >= 4:
        return "HIGH RISK"
    elif score >= 2:
        return "MODERATE RISK"
    elif score >= 1:
        return "LOW RISK"
    else:
        return "NO INDICATORS"

def validate_risk_scores(risk_obj: Dict[str, Any]) -> List[str]:
    """
    Validate risk scores are within valid range (0-5)
    Returns list of validation errors, empty if valid
    """
    errors = []
    risk_dimensions = ["suicide", "homicide", "self_harm", "harm_others"]
    
    for dimension in risk_dimensions:
        if dimension in risk_obj:
            score = risk_obj[dimension].get("score")
            if not isinstance(score, int) or score < 0 or score > 5:
                errors.append(f"Invalid {dimension} risk score: {score}. Must be integer 0-5.")
    
    return errors

def get_risk_summary(risk_obj: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get summary of risk assessment
    Returns dictionary with risk level, highest score, and alert status
    """
    highest_score = get_highest_risk_score(risk_obj)
    risk_level = get_risk_level_description(highest_score)
    has_alert = has_red_alert(risk_obj)
    
    return {
        "highest_score": highest_score,
        "risk_level": risk_level,
        "has_red_alert": has_alert,
        "dimensions": {
            dim: {
                "score": risk_obj[dim].get("score", 0),
                "description": get_risk_level_description(risk_obj[dim].get("score", 0))
            }
            for dim in ["suicide", "homicide", "self_harm", "harm_others"]
            if dim in risk_obj
        }
    }

def get_escalation_recommendations(risk_obj: Dict[str, Any]) -> List[str]:
    """
    Get escalation recommendations based on risk assessment
    Returns list of recommended actions
    """
    recommendations = []
    
    if has_red_alert(risk_obj):
        recommendations.append("IMMEDIATE: Escalate to supervisor")
        recommendations.append("IMMEDIATE: Activate crisis response protocol")
    
    highest_score = get_highest_risk_score(risk_obj)
    
    if highest_score >= 4:
        recommendations.append("HIGH PRIORITY: Schedule immediate follow-up")
        recommendations.append("HIGH PRIORITY: Consider emergency services contact")
    elif highest_score >= 2:
        recommendations.append("MODERATE: Schedule follow-up within 24 hours")
        recommendations.append("MODERATE: Connect with mental health resources")
    elif highest_score >= 1:
        recommendations.append("LOW: Provide ongoing support resources")
        recommendations.append("LOW: Schedule routine follow-up")
    
    return recommendations
