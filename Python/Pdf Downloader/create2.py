from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart

# Create a PDF document
pdf = SimpleDocTemplate("math_club_report.pdf", pagesize=A4)

# Get styles
styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle(
    "TitleStyle",
    parent=styles["Title"],
    fontSize=22,
    textColor=colors.darkblue,
    alignment=1,  # Center alignment
    spaceAfter=20,
)

subtitle_style = ParagraphStyle(
    "SubtitleStyle",
    parent=styles["Heading2"],
    fontSize=14,
    textColor=colors.darkred,
    spaceAfter=10,
)

body_style = styles["BodyText"]

# Cover Page
cover_title = Paragraph("<b>Math Club Activity Report</b>", title_style)
cover_subtitle = Paragraph("Final Report - Last Month", subtitle_style)
cover_text = Paragraph(
    "Prepared by: Math Club Coordinator<br/>Date: February 2025", body_style)

# Change to an actual image
cover_image = Image("math_logo.png", width=100, height=100)

# Activities Table
activities = [
    ["Date", "Activity", "Participants"],
    ["Feb 5", "Math Olympiad Training", "20"],
    ["Feb 10", "Guest Lecture on Algebra", "35"],
    ["Feb 15", "Puzzle Solving Contest", "25"],
    ["Feb 20", "Team Problem-Solving", "30"],
    ["Feb 25", "Math Fun Day", "40"],
]

table = Table(activities, colWidths=[100, 200, 100])
table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("VALIGN", (0, 0), (-1, 0), "MIDDLE"),  # Center vertically in header
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
    ("TOPPADDING", (0, 0), (-1, 0), 10),
    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
    ("GRID", (0, 0), (-1, -1), 1, colors.black),
]))

# Participation Chart
drawing = Drawing(400, 200)
chart = VerticalBarChart()
chart.x = 50
chart.y = 50
chart.height = 125
chart.width = 300
chart.data = [[35, 20, 25, 30, 40]]
chart.categoryAxis.categoryNames = [
    "Feb 5", "Feb 10", "Feb 15", "Feb 20", "Feb 25"]
chart.barSpacing = 5
chart.bars[0].fillColor = colors.blue
drawing.add(chart)

# Report Sections
intro = Paragraph(
    "<b>Introduction</b><br/>This report highlights the activities and participation of our Math Club over the past month.", body_style)
conclusion = Paragraph(
    "<b>Conclusion</b><br/>The Math Club had an exciting and engaging month, with increasing participation. We look forward to next month's activities!", body_style)

# Build PDF
pdf.build([
    cover_title,
    cover_subtitle,
    Spacer(1, 10),
    cover_text,
    cover_image,
    intro,
    Spacer(1, 10),
    table,
    Spacer(1, 10),
    Paragraph("<b>Participation Trends</b>", subtitle_style),
    drawing, Spacer(1, 20),
    conclusion
])
