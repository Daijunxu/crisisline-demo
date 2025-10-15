"""
Pydantic models for API requests/responses
"""

from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class CallResponse(BaseModel):
    call_id: str
    started_at: str
    ended_at: str
    duration_sec: int
    channel: str
    language: str
    timezone: str
    caller_profile: Dict[str, Any]
    turns: List[Dict[str, str]]
    summary: Dict[str, Any]
    risk: Dict[str, Any]
    analytics: Dict[str, Any]

class AnalyticsResponse(BaseModel):
    total_calls: int
    risk_distribution: Dict[int, int]
    avg_response_time: float

class CallsListResponse(BaseModel):
    calls: List[CallResponse]

