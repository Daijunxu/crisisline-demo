"""
Simplified FastAPI Backend for EmpathZ AI Coordinator Demo
Optimized for Vercel deployment
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
import json
import os
from datetime import datetime, timedelta

# Import the PDF generation function
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
    allow_origins=["*"],  # Allow all origins for demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load demo data
def load_demo_calls():
    """Load demo crisis hotline calls data"""
    return [
        {
            "call_id": "CALL-2025-001",
            "started_at": "2025-10-15T09:15:00-07:00",
            "ended_at": "2025-10-15T09:47:00-07:00",
            "duration_sec": 1920,
            "channel": "phone",
            "language": "en",
            "timezone": "America/Los_Angeles",
            "caller_profile": {
                "age_range": "65-70",
                "gender": "female",
                "notes": "Recently widowed, lives alone"
            },
            "turns": [
                {"speaker": "responder", "text": "Crisis hotline, this is Sarah. I'm here to listen. How can I help you today?"},
                {"speaker": "caller", "text": "Hello... I don't know if I should be calling this number. I feel so alone."},
                {"speaker": "responder", "text": "You absolutely should be calling. You're not alone, and I'm glad you reached out. Can you tell me what's going on?"},
                {"speaker": "caller", "text": "My husband passed away six months ago. We were married for 45 years. I just... I don't know how to do this life without him."},
                {"speaker": "responder", "text": "I'm so sorry for your loss. Losing a partner after 45 years must feel unbearable. That's such a long time to build a life together."},
                {"speaker": "caller", "text": "It does. Everything reminds me of him. I can't cook because he was the cook. I can't sleep in our bed because it's too empty. My children try to help, but they have their own lives."},
                {"speaker": "responder", "text": "Grief can feel so overwhelming, especially when it touches every part of your daily routine. What you're experiencing sounds very normal for someone who lost their life partner."},
                {"speaker": "caller", "text": "Sometimes I think it would be easier if I just... if I wasn't here anymore. I'm not saying I would do anything, but the thought crosses my mind."},
                {"speaker": "responder", "text": "I'm glad you shared that with me. Those thoughts are common when grief feels overwhelming. Can you tell me more about what makes you feel like you want to keep going?"},
                {"speaker": "caller", "text": "My grandchildren. They're the only thing that makes me smile anymore. But they live far away, and I only see them on video calls."},
                {"speaker": "responder", "text": "Your grandchildren sound like they bring you joy. That connection to the future, to love continuing - that's so important. Have you considered reaching out to grief support groups in your area?"},
                {"speaker": "caller", "text": "I've thought about it, but I'm not good with groups. I'm shy around strangers."},
                {"speaker": "responder", "text": "That's completely understandable. There are other options too - one-on-one counseling, online support, or even just calling us here when you need someone to listen. You don't have to go through this alone."},
                {"speaker": "caller", "text": "You're so kind. Just talking to you right now helps. I haven't talked about him much since he died."},
                {"speaker": "responder", "text": "Talking about your husband, sharing your memories and your pain - that's part of healing. His memory lives on through you and through your children and grandchildren."},
                {"speaker": "caller", "text": "I have this photo album I've been meaning to look through, but I've been too afraid. Maybe I should try that."},
                {"speaker": "responder", "text": "That sounds like a beautiful way to honor his memory. You could start small - maybe just one photo at a time. And remember, it's okay to cry while you do it."},
                {"speaker": "caller", "text": "Thank you for saying that. I always feel like I should be stronger, but maybe it's okay to not be strong all the time."},
                {"speaker": "responder", "text": "Absolutely. Grief isn't about being strong - it's about feeling your feelings and taking it one day at a time. You're already being incredibly brave by reaching out today."},
                {"speaker": "caller", "text": "I'm glad I called. I was worried you'd think I was being silly."},
                {"speaker": "responder", "text": "Not at all. What you're going through is real and valid. Before we end our call, I want to make sure you have some resources. Do you have a local crisis center or grief counselor you could contact?"},
                {"speaker": "caller", "text": "I have the number for a grief counselor my doctor recommended, but I haven't called yet."},
                {"speaker": "responder", "text": "Would you be willing to make that call this week? I can help you think through what you might want to say."},
                {"speaker": "caller", "text": "Yes, I think I could do that. Maybe I'll call tomorrow."},
                {"speaker": "responder", "text": "That sounds like a good plan. And remember, you can always call us back here if you need to talk. We're available 24/7."},
                {"speaker": "caller", "text": "Thank you so much. You've helped me more than you know."},
                {"speaker": "responder", "text": "I'm so glad we could talk today. Take care of yourself, and remember - you're not alone in this."}
            ],
            "summary": {
                "sections": {
                    "caller_profile": "70-year-old widowed female, recently lost husband of 45 years, lives alone, has adult children and grandchildren but limited local support",
                    "presenting_problem": "Overwhelming grief and loneliness following spouse's death 6 months ago, with passive suicidal ideation but no active plan or intent",
                    "context_timeline": "Husband passed away 6 months ago after 45-year marriage. Caller struggling with daily routines, sleep, and social isolation. Children live far away, limited local support network",
                    "risk_factors": "Recent loss of primary attachment figure, social isolation, disruption of daily routines, passive suicidal ideation, lack of grief support resources",
                    "protective_factors": "Strong connection to grandchildren, willingness to reach out for help, established relationship with healthcare provider, no history of mental health issues or substance use",
                    "interventions": "Active listening, validation of grief experience, psychoeducation about normal grief responses, exploration of protective factors, referral to grief counselor, safety planning around suicidal thoughts",
                    "outcome": "Caller expressed relief and gratitude, committed to contacting grief counselor, agreed to use crisis line for ongoing support, demonstrated improved mood and hope by end of call",
                    "safety_plan": "Caller agreed to contact grief counselor within one week, will use crisis line for ongoing support, identified photo album as positive memory activity, committed to reaching out if suicidal thoughts intensify"
                },
                "tone": "empathetic_professional"
            },
            "risk": {
                "suicide": {"score": 1, "reason_quotes": ["Sometimes I think it would be easier if I just... if I wasn't here anymore. I'm not saying I would do anything, but the thought crosses my mind."], "explanation": "Caller expressed passive suicidal ideation but explicitly stated no intent or plan. Thoughts appear to be grief-related and transient."},
                "homicide": {"score": 0, "reason_quotes": [], "explanation": "No indicators of homicidal ideation or intent. Caller expressed only internal distress and grief."},
                "self_harm": {"score": 0, "reason_quotes": [], "explanation": "No evidence of self-harm behaviors or ideation. Caller's distress appears to be emotional rather than behavioral."},
                "harm_others": {"score": 0, "reason_quotes": [], "explanation": "No indicators of intent or risk to harm others. Caller expressed only grief and loneliness."}
            },
            "analytics": {"response_time_sec": 45, "handled_by": "Agent Sarah"}
        },
        {
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
            "turns": [
                {"speaker": "responder", "text": "Crisis hotline, this is Michael. I'm here to help. What's going on?"},
                {"speaker": "caller", "text": "I don't know what to do. I think I want to die."},
                {"speaker": "responder", "text": "I'm really glad you called and told me that. You're not alone right now. Can you tell me what's making you feel this way?"},
                {"speaker": "caller", "text": "My girlfriend broke up with me yesterday. We were together for two years. She said she doesn't love me anymore and she's already dating someone else."},
                {"speaker": "responder", "text": "That sounds incredibly painful. A two-year relationship ending so suddenly must feel devastating, especially at your age."},
                {"speaker": "caller", "text": "I can't stop thinking about it. I can't eat, I can't sleep. I keep seeing them together in my head. I have a bottle of pills in my room..."},
                {"speaker": "responder", "text": "I'm really concerned about you right now. You mentioned pills - are you thinking about taking them?"},
                {"speaker": "caller", "text": "Yes. I don't want to feel this pain anymore. I've been researching how many to take. I know exactly what to do."},
                {"speaker": "responder", "text": "I'm so glad you called before doing anything. That pain you're feeling is real, but it won't last forever. Can you tell me - do you have the pills with you right now?"},
                {"speaker": "caller", "text": "Yes, they're right here on my desk. I've been looking at them for hours."},
                {"speaker": "responder", "text": "I need you to do something for me right now. Can you put those pills away somewhere safe, maybe in a drawer or give them to a family member?"},
                {"speaker": "caller", "text": "I don't know... I don't want to feel like this anymore."},
                {"speaker": "responder", "text": "I understand you're in a lot of pain right now. But ending your life is permanent, and this pain is temporary. Can you tell me about other people in your life who care about you?"},
                {"speaker": "caller", "text": "My parents, I guess. But they don't understand. They just say I'll get over it. My friends are all busy with their own stuff."},
                {"speaker": "responder", "text": "It sounds like you're feeling really isolated right now. That must make everything feel even worse. Can you tell me more about your parents? Do they know you're struggling?"},
                {"speaker": "caller", "text": "No, I haven't told them. They'll just be disappointed in me. I'm supposed to be strong."},
                {"speaker": "responder", "text": "Reaching out for help when you're hurting isn't weak - it's actually really brave. You showed that by calling me today. I think your parents would want to know you're struggling so they can help."},
                {"speaker": "caller", "text": "Maybe... but what if they don't understand? What if they think I'm overreacting?"},
                {"speaker": "responder", "text": "The pain you're feeling is real and valid. A breakup, especially after two years, is a significant loss. It's okay to not be okay. Can you promise me you'll talk to your parents tonight?"},
                {"speaker": "caller", "text": "I don't know if I can. What if they don't believe me?"},
                {"speaker": "responder", "text": "What if they do? What if they've been waiting for you to reach out? Parents often want to help but don't know how. Can you start by just telling them you're having a really hard time?"},
                {"speaker": "caller", "text": "Okay, maybe I can try that. But what about the pills? I keep thinking about them."},
                {"speaker": "responder", "text": "I'm really concerned about those pills being accessible to you right now. Can you put them somewhere safe, or better yet, give them to your parents to hold onto?"},
                {"speaker": "caller", "text": "I guess I could give them to my mom. She has a locked medicine cabinet."},
                {"speaker": "responder", "text": "That sounds like a really good plan. And when you give them to her, that's also a good time to tell her you're struggling. She'll probably be relieved you're talking to her."},
                {"speaker": "caller", "text": "What if she gets mad or doesn't take me seriously?"},
                {"speaker": "responder", "text": "If she gets upset, it's probably because she's worried about you, not because she's mad at you. Parents often feel scared when their child is in pain. But most parents want to help if they can."},
                {"speaker": "caller", "text": "I hope so. I'm still scared it will happen again."},
                {"speaker": "responder", "text": "That fear is normal. But remember - you just got through one, and you did it by staying calm and using coping skills. You're stronger than you think."},
                {"speaker": "caller", "text": "Do you really think I can get through this?"},
                {"speaker": "responder", "text": "I do. You're already taking the first steps by reaching out for help. That takes courage. Can you tell me what you're going to do when we hang up?"},
                {"speaker": "caller", "text": "Give the pills to my mom and tell her I'm having a hard time. And maybe try to eat something."},
                {"speaker": "responder", "text": "That sounds like a really good plan. And remember, if you start feeling like hurting yourself again, you can always call us back. We're here 24/7."},
                {"speaker": "caller", "text": "Thank you. I'm scared, but I think I can do this."},
                {"speaker": "responder", "text": "Being scared is normal when you're going through something this hard. But you're not alone. You have people who care about you, and you have resources like us. You've got this."},
                {"speaker": "caller", "text": "Thank you for talking to me. I think I would have done something stupid if I hadn't called."},
                {"speaker": "responder", "text": "I'm so glad you called. You made the right choice. Take care of yourself, and remember - this pain is temporary, but your life has value beyond this moment."}
            ],
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
    ]

# Load calls data
calls_data = load_demo_calls()

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

# Vercel handler
def handler(request):
    return app(request.scope, request.receive, request.send)
