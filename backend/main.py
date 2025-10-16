"""
FastAPI Backend for EmpathZ AI Coordinator Demo
Serves REST API endpoints for crisis hotline call analysis
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
import tempfile
import os
from typing import List, Dict, Any

from data_demo import load_all_calls
from logic.pdf_report import generate_call_report, get_report_filename

# Create FastAPI app
app = FastAPI(
    title="EmpathZ AI Coordinator API",
    description="REST API for crisis hotline call analysis and risk assessment",
    version="1.0.0"
)

# Add CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:3001",
        "http://localhost:3002",
        "http://localhost:5173",
        "https://*.vercel.app",  # Vercel preview deployments
        "https://crisisline-demo-ijrzkxafm-daijuns-projects-0957a011.vercel.app",  # Current deployment
        "https://empathz-demo.vercel.app"  # Production domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load all calls at startup
calls_data = load_all_calls()

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "EmpathZ AI Coordinator API", "version": "1.0.0"}

@app.get("/api/calls")
async def get_all_calls():
    """Get all crisis hotline calls"""
    return {"calls": calls_data}

@app.get("/api/calls/{call_id}")
async def get_call(call_id: str):
    """Get a specific call by ID"""
    call = next((call for call in calls_data if call["call_id"] == call_id), None)
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    return call

@app.get("/api/analytics")
async def get_analytics():
    """Get dashboard analytics"""
    # Simple analytics computation
    total_calls = len(calls_data)
    risk_distribution = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
    total_response_time = 0
    
    for call in calls_data:
        max_risk = 0
        if 'risk' in call:
            max_risk = max(
                call['risk'].get('suicide', {}).get('score', 0),
                call['risk'].get('homicide', {}).get('score', 0),
                call['risk'].get('self_harm', {}).get('score', 0),
                call['risk'].get('harm_others', {}).get('score', 0)
            )
        risk_distribution[str(max_risk)] += 1
        
        if 'analytics' in call and 'response_time_sec' in call['analytics']:
            total_response_time += call['analytics']['response_time_sec']
    
    avg_response_time = total_response_time / total_calls if total_calls > 0 else 0
    
    return {
        "total_calls": total_calls,
        "risk_distribution": risk_distribution,
        "avg_response_time": avg_response_time
    }

@app.get("/api/calls/{call_id}/pdf")
async def download_pdf(call_id: str):
    """Download PDF report for a specific call"""
    call = next((call for call in calls_data if call["call_id"] == call_id), None)
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    
    try:
        # Generate PDF
        pdf_content = generate_call_report(call)
        filename = get_report_filename(call_id)
        
        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
