from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import ListFlowable, SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, ListItem
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT


def create_math_club_pdf(filename, data):
    if Path(filename).exists():
        Path(filename).unlink()
    """Creates a PDF for a math club establishment record."""

    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    # Create a style for the title
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['h1'],
        alignment=TA_CENTER
    )  # Inherit from h1
    p_style = ParagraphStyle(
        'PStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10
    )  # Inherit from p
    story = []

    # Title (French)
    title = Paragraph(
        "Procès-verbal de constitution d'un club", title_style)
    story.append(title)
    story.append(Spacer(1, 12))

    # Subject (French)
    subject = Paragraph(f"Date : {data['date']}", styles['h2'])
    story.append(subject)
    subject = Paragraph(f"Etablissement : {data['school_name']}", styles['h2'])
    story.append(subject)
    subject = Paragraph(
        "Objet : Constitution du club des mathématiques", styles['h2'])
    story.append(subject)
    story.append(Spacer(1, 12))

    agenda_title = Paragraph("Liste des Membres :", styles['h2'])
    story.append(agenda_title)
    story.append(Spacer(1, 5))
    # Attendance (Table - French headers)
    attendance_data = [["Nom", "Rôle"]] + [[e.title(), t]
                                           for e, t in data['attendance']]
    attendance_table = Table(attendance_data)
    attendance_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 2),
        ('TOPPADDING', (0, 0), (-1, 0), 2),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(attendance_table)
    story.append(Spacer(1, 12))

    # Agenda (French)
    agenda_title = Paragraph("Objectifs du club :", styles['h2'])
    story.append(agenda_title)

    list_items = []  # Create an empty list to hold ListItems
    for item in data['agenda']:
        # Create and add ListItem
        list_items.append(
            ListItem(Paragraph(f"{item.capitalize()} .", p_style)))

    # Pass the list to ListFlowable <--- Corrected
    agenda_list = ListFlowable(list_items, bulletType='bullet')

    story.append(agenda_list)

    doc.build(story)


def create_math_club_program(filename, data):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()

    # Title Style
    title_style = ParagraphStyle('TitleStyle', parent=styles['h1'])
    title_style.alignment = TA_CENTER
    title_style.textColor = colors.green
    p_style = ParagraphStyle(
        'PStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
    )  # Inherit from p

    # Activity Title Style
    activity_title_style = ParagraphStyle('ActivityTitle', parent=styles['h2'])
    activity_title_style.alignment = TA_LEFT
    activity_title_style.textColor = colors.cyan
    activity_title_style.fontName = 'Helvetica-Bold'

    # Description Style
    description_style = ParagraphStyle('Description', parent=styles['Normal'])
    description_style.alignment = TA_LEFT

    story = []

    # Title
    for titre in data['titles']:
        title = Paragraph(titre, title_style)
        story.append(title)
        story.append(Spacer(1, 7))

    # Introduction (Optional)
    if 'introduction' in data:
        intro = Paragraph(data['introduction'], p_style)
        story.append(intro)
        story.append(Spacer(1, 12))

    # Activities
    for activity in data['activities']:
        activity_title = Paragraph(
            activity['title'].capitalize() + " :", activity_title_style)
        story.append(activity_title)
        story.append(Spacer(1, 4))

        description = Paragraph(
            activity['description'].capitalize(), description_style)
        story.append(description)
        story.append(Spacer(1, 4))

        # Add details if available (e.g., date, time, location)
        if 'details' in activity:
            list_items = []  # Create an empty list to hold ListItems
            for detail in activity['details']:
                list_items.append(
                    ListItem(Paragraph(detail.capitalize(), p_style)))
            details_list = ListFlowable(list_items, bulletType='bullet')
            story.append(details_list)
            story.append(Spacer(1, 12))  # Space after each activity

    doc.build(story)


styles = getSampleStyleSheet()
filename = "test.pdf"
doc = SimpleDocTemplate(filename, pagesize=letter)
descriptions = [Paragraph('- Description', styles['Bullet']) for _ in range(5)]
story = []
for p in descriptions:
    story.append(p)
    story.append(Spacer(1, 15))
doc.build(story)
