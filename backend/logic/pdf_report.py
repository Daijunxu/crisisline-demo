"""
PDF Report Generation for EmpathZ AI Coordinator
Generates professional PDF reports for crisis hotline calls
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.colors import HexColor, black, grey
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.barcharts import HorizontalBarChart
from reportlab.graphics import renderPDF
from datetime import datetime, timedelta
import io


def generate_call_report(call_data):
    """
    Generate a PDF report for a crisis hotline call matching the exact format shown
    
    Args:
        call_data (dict): Call data including transcript, summary, and risk assessment
        
    Returns:
        bytes: PDF file content as bytes
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=72)
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Custom styles matching the design
    main_title_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Normal'],
        fontSize=24,
        spaceAfter=12,
        alignment=TA_CENTER,
        textColor=HexColor('#1E40AF'),  # Blue
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=16,
        spaceAfter=12,
        alignment=TA_CENTER,
        textColor=HexColor('#000000'),
        fontName='Helvetica'
    )
    
    call_info_header_style = ParagraphStyle(
        'CallInfoHeader',
        parent=styles['Normal'],
        fontSize=14,
        spaceAfter=12,
        alignment=TA_CENTER,
        textColor=HexColor('#000000'),
        fontName='Helvetica'
    )
    
    section_heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=20,
        textColor=HexColor('#000000'),
        fontName='Helvetica-Bold'
    )
    
    subsection_heading_style = ParagraphStyle(
        'SubsectionHeading',
        parent=styles['Heading3'],
        fontSize=12,
        spaceAfter=6,
        spaceBefore=12,
        textColor=HexColor('#000000'),
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=8,
        alignment=TA_LEFT,
        textColor=HexColor('#000000'),
        fontName='Helvetica'
    )
    
    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        parent=styles['Normal'],
        fontSize=9,
        spaceAfter=12,
        alignment=TA_CENTER,
        textColor=HexColor('#666666'),
        fontName='Helvetica'
    )
    
    # Build the story (content)
    story = []
    
    # Header
    story.append(Paragraph("EmpathZ for Crisis Hotline", main_title_style))
    story.append(Paragraph("AI-Generated Case Report", subtitle_style))
    story.append(Spacer(1, 20))
    
    # Call ID and Date
    call_date = datetime.fromisoformat(call_data['started_at'].replace('Z', '+00:00'))
    date_str = call_date.strftime('%B %d, %Y')
    story.append(Paragraph(f"Call ID: {call_data['call_id']} | Date: {date_str}", call_info_header_style))
    story.append(Spacer(1, 30))
    
    # Call Information Section
    story.append(Paragraph("Call Information", section_heading_style))
    
    # Create call information table
    duration_min = call_data['duration_sec'] // 60
    duration_sec = call_data['duration_sec'] % 60
    duration_str = f"{duration_min:02d}:{duration_sec:02d}"
    
    start_time = call_date.strftime('%I:%M %p')
    end_time = (call_date + timedelta(seconds=call_data['duration_sec'])).strftime('%I:%M %p')
    
    profile = call_data.get('caller_profile', {})
    analytics = call_data.get('analytics', {})
    
    call_info_data = [
        ['Call Duration:', duration_str],
        ['Start Time:', start_time],
        ['End Time:', end_time],
        ['Channel:', call_data['channel'].title()],
        ['Age Range:', profile.get('age_range', 'Not specified')],
        ['Gender:', profile.get('gender', 'Not specified').title()],
        ['Handled By:', analytics.get('handled_by', 'Not specified')]
    ]
    
    call_info_table = Table(call_info_data, colWidths=[2*inch, 3*inch])
    call_info_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    
    story.append(call_info_table)
    story.append(Spacer(1, 20))
    
    # Case Summary Section
    story.append(Paragraph("Case Summary", section_heading_style))
    
    if 'summary' in call_data and 'sections' in call_data['summary']:
        sections = call_data['summary']['sections']
        
        # Define the order and display names for sections
        section_order = [
            ('caller_profile', 'Caller Profile'),
            ('presenting_problem', 'Presenting Problem'),
            ('context_timeline', 'Context & Timeline'),
            ('risk_factors', 'Risk Factors'),
            ('protective_factors', 'Protective Factors'),
            ('interventions', 'Interventions Provided'),
            ('outcome', 'Outcome'),
            ('safety_plan', 'Safety Plan & Referrals')
        ]
        
        for section_key, section_title in section_order:
            if section_key in sections and sections[section_key]:
                story.append(Paragraph(section_title, subsection_heading_style))
                
                # Format risk factors and protective factors as bullet points
                if section_key in ['risk_factors', 'protective_factors']:
                    items = sections[section_key].split(', ')
                    for item in items:
                        if item.strip():
                            story.append(Paragraph(f"• {item.strip()}", body_style))
                else:
                    story.append(Paragraph(sections[section_key], body_style))
    
    story.append(Spacer(1, 20))
    
    # Risk Assessment Section
    story.append(Paragraph("Risk Assessment", section_heading_style))
    
    if 'risk' in call_data:
        risk_data = call_data['risk']
        
        # Risk type display names
        risk_display_names = {
            'suicide': 'Suicide Risk',
            'homicide': 'Homicide Risk', 
            'self_harm': 'Self-Harm Risk',
            'harm_others': 'Harm to Others'
        }
        
        for risk_type, data in risk_data.items():
            if risk_type in risk_display_names:
                score = data.get('score', 0)
                risk_title = risk_display_names[risk_type]
                
                story.append(Paragraph(f"{risk_title}: {score}/5", subsection_heading_style))
                
                # Create risk bar chart
                drawing = Drawing(400, 30)
                bar_chart = HorizontalBarChart()
                bar_chart.x = 0
                bar_chart.y = 0
                bar_chart.height = 20
                bar_chart.width = 400
                bar_chart.data = [[score, 5-score]]
                bar_chart.bars[0].fillColor = HexColor('#FF6B35')  # Orange
                bar_chart.bars[1].fillColor = HexColor('#E5E5E5')  # Gray
                bar_chart.barSpacing = 2
                bar_chart.categoryAxis.categoryNames = ['']
                bar_chart.valueAxis.valueMin = 0
                bar_chart.valueAxis.valueMax = 5
                bar_chart.valueAxis.valueStep = 1
                bar_chart.valueAxis.labels.fontSize = 8
                drawing.add(bar_chart)
                story.append(drawing)
                
                # Risk explanation
                if data.get('explanation'):
                    story.append(Paragraph(data['explanation'], body_style))
                
                # Risk quotes
                if data.get('reason_quotes'):
                    for quote in data['reason_quotes']:
                        if quote.strip():
                            story.append(Paragraph(f'"{quote.strip()}"', 
                                                 ParagraphStyle('Quote', parent=body_style, leftIndent=20, fontStyle='italic')))
                
                story.append(Spacer(1, 12))
    
    # Disclaimer
    story.append(Spacer(1, 30))
    story.append(Paragraph("DISCLAIMER: This report was generated using AI technology for demonstration purposes. This is not real patient data and should not be used for clinical decision-making. © 2025 EmpathZ Demo v1.0", disclaimer_style))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def get_report_filename(call_id):
    """Generate filename for the PDF report"""
    date_str = datetime.now().strftime('%Y%m%d')
    return f"EmpathZ_CaseReport_{call_id}_{date_str}.pdf"
