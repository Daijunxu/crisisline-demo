"""
FastAPI Backend for EmpathZ AI Coordinator Demo
Serves REST API endpoints for crisis hotline call analysis
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import tempfile
import os
from typing import List, Dict, Any

from api.routes import router
from data_demo import load_all_calls
from logic.analytics import compute_analytics
from logic.pdf_report import generate_pdf_report, create_download_filename

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
        "https://empathz-demo.vercel.app"  # Production domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

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
    analytics = compute_analytics(calls_data)
    return analytics

@app.get("/api/calls/{call_id}/pdf")
async def download_pdf(call_id: str):
    """Download PDF report for a specific call"""
    call = next((call for call in calls_data if call["call_id"] == call_id), None)
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    
    try:
        # Generate PDF
        filename = create_download_filename(call)
        temp_path = os.path.join(tempfile.gettempdir(), filename)
        
        pdf_path = generate_pdf_report(call, temp_path)
        
        return FileResponse(
            path=pdf_path,
            filename=filename,
            media_type="application/pdf"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
