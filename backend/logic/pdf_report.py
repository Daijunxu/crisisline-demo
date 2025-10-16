"""
PDF Report Generation for EmpathZ AI Coordinator
Generates professional PDF reports for crisis hotline calls
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.colors import HexColor, black
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import io


def generate_call_report(call_data):
    """
    Generate a PDF report for a crisis hotline call
    
    Args:
        call_data (dict): Call data including transcript, summary, and risk assessment
        
    Returns:
        bytes: PDF file content as bytes
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=HexColor('#1E40AF')  # Blue color
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor=HexColor('#374151')  # Dark gray
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        alignment=TA_JUSTIFY,
        leftIndent=0,
        rightIndent=0
    )
    
    transcript_style = ParagraphStyle(
        'Transcript',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=4,
        leftIndent=20,
        rightIndent=20
    )
    
    # Build the story (content)
    story = []
    
    # Title
    story.append(Paragraph("EmpathZ AI Coordinator", title_style))
    story.append(Paragraph("Crisis Hotline Call Report", title_style))
    story.append(Spacer(1, 12))
    
    # Call Information
    story.append(Paragraph("Call Information", heading_style))
    story.append(Paragraph(f"<b>Call ID:</b> {call_data['call_id']}", body_style))
    story.append(Paragraph(f"<b>Date:</b> {call_data['started_at'][:10]}", body_style))
    story.append(Paragraph(f"<b>Time:</b> {call_data['started_at'][11:19]}", body_style))
    story.append(Paragraph(f"<b>Duration:</b> {call_data['duration_sec'] // 60} minutes {call_data['duration_sec'] % 60} seconds", body_style))
    story.append(Paragraph(f"<b>Channel:</b> {call_data['channel'].title()}", body_style))
    story.append(Paragraph(f"<b>Language:</b> {call_data['language'].upper()}", body_style))
    story.append(Spacer(1, 12))
    
    # Caller Profile
    if 'caller_profile' in call_data:
        story.append(Paragraph("Caller Profile", heading_style))
        profile = call_data['caller_profile']
        story.append(Paragraph(f"<b>Age Range:</b> {profile.get('age_range', 'Not specified')}", body_style))
        story.append(Paragraph(f"<b>Gender:</b> {profile.get('gender', 'Not specified').title()}", body_style))
        if profile.get('notes'):
            story.append(Paragraph(f"<b>Notes:</b> {profile['notes']}", body_style))
        story.append(Spacer(1, 12))
    
    # Case Summary
    if 'summary' in call_data and 'sections' in call_data['summary']:
        story.append(Paragraph("Case Summary", heading_style))
        sections = call_data['summary']['sections']
        
        for section_name, content in sections.items():
            if content:  # Only include non-empty sections
                section_title = section_name.replace('_', ' ').title()
                story.append(Paragraph(f"<b>{section_title}:</b>", body_style))
                story.append(Paragraph(content, body_style))
                story.append(Spacer(1, 6))
        story.append(Spacer(1, 12))
    
    # Risk Assessment
    if 'risk' in call_data:
        story.append(Paragraph("Risk Assessment", heading_style))
        risk_data = call_data['risk']
        
        risk_colors = {
            'suicide': '#DC2626',  # Red
            'homicide': '#DC2626',  # Red
            'self_harm': '#D97706',  # Orange
            'harm_others': '#D97706'  # Orange
        }
        
        for risk_type, data in risk_data.items():
            risk_title = risk_type.replace('_', ' ').title()
            score = data.get('score', 0)
            color = risk_colors.get(risk_type, '#374151')
            
            # Risk level text
            if score <= 1:
                level = "Low"
            elif score <= 3:
                level = "Moderate"
            else:
                level = "High"
            
            story.append(Paragraph(f"<b>{risk_title}:</b> Score {score}/5 - {level}", body_style))
            if data.get('explanation'):
                story.append(Paragraph(data['explanation'], body_style))
            story.append(Spacer(1, 6))
        story.append(Spacer(1, 12))
    
    # Page break before transcript
    story.append(PageBreak())
    
    # Call Transcript
    if 'turns' in call_data:
        story.append(Paragraph("Call Transcript", heading_style))
        story.append(Spacer(1, 12))
        
        for i, turn in enumerate(call_data['turns']):
            speaker = "Caller" if turn['speaker'] == 'caller' else "Responder"
            story.append(Paragraph(f"<b>{speaker}:</b>", transcript_style))
            story.append(Paragraph(turn['text'], transcript_style))
            story.append(Spacer(1, 8))
    
    # Footer
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                          ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9, alignment=TA_CENTER)))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def get_report_filename(call_id):
    """Generate filename for the PDF report"""
    date_str = datetime.now().strftime('%Y%m%d')
    return f"EmpathZ_CaseReport_{call_id}_{date_str}.pdf"
