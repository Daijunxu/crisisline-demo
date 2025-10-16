"""
Simple PDF Generation API for Vercel
"""

from http.server import BaseHTTPRequestHandler
import json
import sys
import os
import urllib.parse

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))

try:
    from logic.pdf_report import generate_call_report, get_report_filename
except ImportError:
    # Fallback if imports fail
    def generate_call_report(call_data):
        return b"PDF generation not available"
    def get_report_filename(call_id):
        return f"report_{call_id}.pdf"

# Demo data
DEMO_CALL = {
    "call_id": "CALL-2025-002",
    "started_at": "2025-10-15T14:30:00-07:00",
    "ended_at": "2025-10-15T15:22:00-07:00",
    "duration_sec": 3120,
    "channel": "phone",
    "language": "en",
    "timezone": "America/Los_Angeles",
    "caller_profile": {
        "age_range": "16-17",
        "gender": "male",
        "notes": "High school student, recent breakup"
    },
    "summary": {
        "sections": {
            "caller_profile": "16-year-old male high school student experiencing acute crisis following recent breakup with girlfriend of 2 years",
            "presenting_problem": "Active suicidal ideation with specific plan involving prescription pills, immediate access to means, following devastating breakup",
            "context_timeline": "Girlfriend broke up yesterday after 2-year relationship, caller discovered she is already dating someone else. Has been researching lethal doses and has pills readily available",
            "risk_factors": "Active suicidal ideation with specific plan, access to lethal means, acute emotional distress, social isolation, perceived lack of parental support, recent significant loss",
            "protective_factors": "Intact family system, willingness to call crisis line, ability to engage in safety planning, no prior suicide attempts, strong connection to parents despite perceived barriers",
            "interventions": "Immediate safety planning including removal of lethal means, engagement of family support system, validation of emotional pain, crisis intervention techniques, referral for ongoing mental health support",
            "outcome": "Caller agreed to safety plan including giving pills to parent and disclosing distress to family. Committed to ongoing support and demonstrated decreased immediate risk by end of call",
            "safety_plan": "Immediate: Remove pills from easy access by giving to parent. Short-term: Disclose emotional distress to parents, establish family support system. Long-term: Connect with mental health resources for ongoing support"
        },
        "tone": "empathetic_professional"
    },
    "risk": {
        "suicide": {"score": 4, "reason_quotes": ["I think I want to die.", "I have a bottle of pills in my room... I don't want to feel this pain anymore. I've been researching how many to take. I know exactly what to do.", "Yes, they're right here on my desk. I've been looking at them for hours."], "explanation": "Caller expressed active suicidal ideation with specific plan involving prescription pills. Has immediate access to lethal means and has researched lethal doses. Risk level elevated due to plan specificity and means access."},
        "homicide": {"score": 0, "reason_quotes": [], "explanation": "No indicators of homicidal ideation or intent. Caller's distress is focused internally and on relationship loss."},
        "self_harm": {"score": 2, "reason_quotes": ["I can't eat, I can't sleep. I keep seeing them together in my head."], "explanation": "Evidence of self-neglect behaviors (not eating, sleeping) but no evidence of direct self-harm behaviors or ideation beyond suicidal thoughts."},
        "harm_others": {"score": 0, "reason_quotes": [], "explanation": "No indicators of intent or risk to harm others. Caller's distress is focused on personal loss and internal pain."}
    },
    "analytics": {"response_time_sec": 12, "handled_by": "Agent Michael"}
}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Set CORS headers
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.send_header('Content-type', 'application/pdf')
            
            # Generate PDF
            pdf_content = generate_call_report(DEMO_CALL)
            filename = get_report_filename(DEMO_CALL["call_id"])
            
            self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
            self.end_headers()
            self.wfile.write(pdf_content)
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
