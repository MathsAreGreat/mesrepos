from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER


def create_invoice(filename="invoice.pdf"):
    # Create the PDF doc with margins
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=20*mm,
        leftMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=20*mm,
        title="Liu Young Electronics",
        author="Samo Haung"
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['h1'],
        alignment=TA_CENTER,
        textColor=colors.blueviolet,
    )  # Inherit from h1

    content_style = ParagraphStyle(
        "BodyStyle",
        backColor=colors.blueviolet,
        borderColor=colors.black,
        borderPadding=2,
        borderWidth=1,
        fontName='Helvetica',
        fontSize=10,
    )  # Inherit from h1
    title = Paragraph(
        "Procès-verbal du club", title_style)
    content = Paragraph(
        """
<b>Invoice No:</b> Hgdl165-n<br/>
<b>Date:</b> 21 December 2017<br/>
<b>Payment Terms:</b> 30 days<br/>
<b>VAT Number:</b> 5864194964<br/>
<b>Purchase ID:</b> RPLUS 10k pages
""", content_style)
    # Basic styles
    story = []
    story.append(title)
    story.append(Spacer(1, 5))  # Small spacing
    story.append(content)

    doc.build(story)
    print(f"Invoice '{filename}' created successfully!")


if __name__ == "__main__":
    create_invoice("improve.pdf")
