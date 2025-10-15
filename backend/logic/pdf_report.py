"""
PDF Report Generator for EmpathZ AI Coordinator Demo
Uses ReportLab to generate professional case reports with risk bar visualization
"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
from typing import Dict, Any, List
import os

def generate_pdf_report(call: Dict[str, Any], output_path: str) -> str:
    """
    Generate a professional PDF report for a crisis call
    Returns the path to the generated PDF file
    """
    # Create the PDF document
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Build the story (content)
    story = []
    
    # Header
    story.extend(draw_header(call, styles))
    story.append(Spacer(1, 20))
    
    # Call Information
    story.extend(draw_call_info(call, styles))
    story.append(Spacer(1, 20))
    
    # Summary sections
    story.extend(draw_summary_sections(call["summary"], styles))
    story.append(Spacer(1, 20))
    
    # Risk evaluation with visual bars
    story.extend(draw_risk_section(call["risk"], styles))
    story.append(Spacer(1, 20))
    
    # Footer
    story.extend(draw_footer(styles))
    
    # Build the PDF
    doc.build(story)
    
    return output_path

def draw_header(call: Dict[str, Any], styles) -> List:
    """Draw the report header with organization branding"""
    story = []
    
    # Organization name and tagline
    org_style = ParagraphStyle(
        'OrgHeader',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=12,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#2563eb')
    )
    
    story.append(Paragraph("EmpathZ for Crisis Hotline", org_style))
    
    # Report title
    title_style = ParagraphStyle(
        'ReportTitle',
        parent=styles['Heading2'],
        fontSize=18,
        spaceAfter=12,
        alignment=TA_CENTER
    )
    
    story.append(Paragraph("AI-Generated Case Report", title_style))
    
    # Call ID and date
    call_id = call.get("call_id", "Unknown")
    call_date = datetime.fromisoformat(call.get("started_at", "")).strftime("%B %d, %Y")
    
    info_style = ParagraphStyle(
        'CallInfo',
        parent=styles['Normal'],
        fontSize=12,
        alignment=TA_CENTER,
        textColor=colors.grey
    )
    
    story.append(Paragraph(f"Call ID: {call_id} | Date: {call_date}", info_style))
    
    return story

def draw_call_info(call: Dict[str, Any], styles) -> List:
    """Draw call information table"""
    story = []
    
    # Call information header
    header_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading3'],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.HexColor('#374151')
    )
    
    story.append(Paragraph("Call Information", header_style))
    
    # Create call info table
    started_at = datetime.fromisoformat(call.get("started_at", "")).strftime("%I:%M %p")
    ended_at = datetime.fromisoformat(call.get("ended_at", "")).strftime("%I:%M %p")
    duration_min = call.get("duration_sec", 0) // 60
    duration_sec = call.get("duration_sec", 0) % 60
    
    caller_profile = call.get("caller_profile", {})
    age_range = caller_profile.get("age_range", "Not specified")
    gender = caller_profile.get("gender", "Not specified")
    
    data = [
        ["Call Duration:", f"{duration_min}:{duration_sec:02d}"],
        ["Start Time:", started_at],
        ["End Time:", ended_at],
        ["Channel:", call.get("channel", "Unknown").title()],
        ["Age Range:", age_range],
        ["Gender:", gender.title() if gender != "Not specified" else "Not specified"],
        ["Handled By:", call.get("analytics", {}).get("handled_by", "Unknown")]
    ]
    
    table = Table(data, colWidths=[2*inch, 3*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (1, 0), (1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb'))
    ]))
    
    story.append(table)
    return story

def draw_summary_sections(summary: Dict[str, Any], styles) -> List:
    """Draw the case summary sections"""
    story = []
    
    # Summary header
    header_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading3'],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.HexColor('#374151')
    )
    
    story.append(Paragraph("Case Summary", header_style))
    
    sections = summary.get("sections", {})
    section_order = [
        "caller_profile",
        "presenting_problem", 
        "context_timeline",
        "risk_factors",
        "protective_factors",
        "interventions",
        "outcome",
        "safety_plan"
    ]
    
    section_titles = {
        "caller_profile": "Caller Profile",
        "presenting_problem": "Presenting Problem",
        "context_timeline": "Context & Timeline", 
        "risk_factors": "Risk Factors",
        "protective_factors": "Protective Factors",
        "interventions": "Interventions Provided",
        "outcome": "Outcome",
        "safety_plan": "Safety Plan & Referrals"
    }
    
    for section_key in section_order:
        if section_key in sections and sections[section_key]:
            # Section title
            title_style = ParagraphStyle(
                'SubsectionTitle',
                parent=styles['Heading4'],
                fontSize=12,
                spaceAfter=6,
                spaceBefore=12,
                textColor=colors.HexColor('#4b5563')
            )
            
            story.append(Paragraph(section_titles.get(section_key, section_key.replace("_", " ").title()), title_style))
            
            # Section content
            content_style = ParagraphStyle(
                'SummaryContent',
                parent=styles['Normal'],
                fontSize=10,
                spaceAfter=8,
                leftIndent=12
            )
            
            story.append(Paragraph(sections[section_key], content_style))
    
    return story

def draw_risk_section(risk: Dict[str, Any], styles) -> List:
    """Draw the risk evaluation section with visual bars"""
    story = []
    
    # Risk assessment header
    header_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading3'],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.HexColor('#374151')
    )
    
    story.append(Paragraph("Risk Assessment", header_style))
    
    # Check for RED alert
    has_red = any(risk[dim].get("score", 0) >= 4 for dim in ["suicide", "homicide", "self_harm", "harm_others"])
    
    if has_red:
        alert_style = ParagraphStyle(
            'Alert',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#dc2626'),
            backColor=colors.HexColor('#fef2f2'),
            borderWidth=1,
            borderColor=colors.HexColor('#fecaca'),
            borderPadding=8,
            spaceAfter=12,
            alignment=TA_CENTER
        )
        story.append(Paragraph("⚠️ HIGH RISK - ESCALATE TO SUPERVISOR", alert_style))
    
    # Risk dimensions
    dimensions = {
        "suicide": "Suicide Risk",
        "homicide": "Homicide Risk", 
        "self_harm": "Self-Harm Risk",
        "harm_others": "Harm to Others"
    }
    
    for dim_key, dim_name in dimensions.items():
        if dim_key in risk:
            score = risk[dim_key].get("score", 0)
            explanation = risk[dim_key].get("explanation", "")
            quotes = risk[dim_key].get("reason_quotes", [])
            
            # Risk dimension title
            title_style = ParagraphStyle(
                'RiskTitle',
                parent=styles['Heading4'],
                fontSize=11,
                spaceAfter=6,
                spaceBefore=10,
                textColor=colors.HexColor('#4b5563')
            )
            
            story.append(Paragraph(f"{dim_name}: {score}/5", title_style))
            
            # Risk bar visualization
            story.extend(draw_risk_bar_pdf(score))
            story.append(Spacer(1, 8))
            
            # Explanation
            if explanation:
                explanation_style = ParagraphStyle(
                    'RiskExplanation',
                    parent=styles['Normal'],
                    fontSize=9,
                    spaceAfter=6,
                    leftIndent=12
                )
                story.append(Paragraph(explanation, explanation_style))
            
            # Quotes
            if quotes:
                quotes_style = ParagraphStyle(
                    'RiskQuotes',
                    parent=styles['Normal'],
                    fontSize=9,
                    spaceAfter=8,
                    leftIndent=12,
                    textColor=colors.HexColor('#6b7280'),
                    fontStyle='italic'
                )
                for quote in quotes:
                    story.append(Paragraph(f'"{quote}"', quotes_style))
    
    return story

def draw_risk_bar_pdf(score: int) -> List:
    """Draw a visual risk bar in the PDF"""
    from reportlab.platypus import Table
    
    # Create table data - single row with 5 columns
    data = [['', '', '', '', '']]  # Empty strings for each cell
    
    # Create table for visual bar
    table = Table(data, colWidths=[0.8*inch] * 5, rowHeights=[0.2*inch])
    
    # Apply colors to each cell
    table_style = [
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
        ('FONTSIZE', (0, 0), (-1, -1), 6),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ]
    
    # Add background colors for each segment
    for i in range(5):
        if i < score:
            if score >= 4:
                color = colors.HexColor('#dc2626')
            elif score >= 2:
                color = colors.HexColor('#f59e0b')
            else:
                color = colors.HexColor('#10b981')
        else:
            color = colors.HexColor('#e5e7eb')
        
        table_style.append(('BACKGROUND', (i, 0), (i, 0), color))
    
    table.setStyle(TableStyle(table_style))
    
    return [table]

def draw_footer(styles) -> List:
    """Draw the report footer with disclaimer"""
    story = []
    
    story.append(Spacer(1, 40))
    
    # Disclaimer
    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#6b7280'),
        alignment=TA_CENTER,
        spaceBefore=20
    )
    
    disclaimer_text = """
    <b>DISCLAIMER:</b> This report was generated using AI technology for demonstration purposes. 
    This is not real patient data and should not be used for clinical decision-making. 
    © 2025 EmpathZ Demo v1.0
    """
    
    story.append(Paragraph(disclaimer_text, disclaimer_style))
    
    return story

def create_download_filename(call: Dict[str, Any]) -> str:
    """Create a standardized filename for the PDF download"""
    call_id = call.get("call_id", "UNKNOWN")
    date_str = datetime.now().strftime("%Y%m%d")
    return f"EmpathZ_CaseReport_{call_id}_{date_str}.pdf"
