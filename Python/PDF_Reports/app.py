from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from textwrap import dedent
from reportlab.lib.enums import TA_CENTER


def create_invoice(filename):
    # Create the PDF doc with margins
    doc = SimpleDocTemplate(
        filename,
        pagesize=landscape(A4),
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
    title = Paragraph(
        "Procès-verbal du club", title_style)
    # Basic styles
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(name='Right', fontName='Helvetica',
               fontSize=10, leading=12, alignment=0))
    styles.add(ParagraphStyle(name='DueNote', fontName='Helvetica-Bold', fontSize=10, leading=12,
                              textColor=colors.HexColor('#D9534F')))

    story = []
    story.append(title)
    story.append(Spacer(1, 5))  # Small spacing

    # Create an underline as a single-row table
    line = Table([[""]], colWidths=[doc.width],
                 rowHeights=[1])  # Increase row height
    line.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.black),  # Black line
    ]))

    story.append(line)
    story.append(Spacer(1, 10))

    # -- Top Section: Company + Invoice Details --
    left_text = dedent("""\
        <b>Liu Young Electronics</b><br/>
        14 Kings Street, Yang Region<br/>
        Hong Kong<br/>
        Requested by: Samo Haung
    """)
    right_text = dedent("""\
        <b>Invoice No:</b> Hgdl165-n<br/>
        <b>Date:</b> 21 December 2017<br/>
        <b>Payment Terms:</b> 30 days<br/>
        <b>VAT Number:</b> 5864194964<br/>
        <b>Purchase ID:</b> RPLUS 10k pages
    """)
    top_data = [
        [
            Paragraph(left_text, styles['Normal']),
            Paragraph(right_text, styles['Right'])
        ]
    ]
    top_table = Table(top_data, colWidths=[3 * doc.width/4, doc.width/4])
    top_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(top_table)
    story.append(Spacer(1, 12))

    # -- Items Table (full available width, darker blue header, no vertical lines) --
    items_data = [
        ["Description", "Unit Price", "Qty", "Net", "VAT", "Gross"],
        ["RPTLAB PLUS", "£500.00", "1", "£500.00", "20%", "£600.00"],
        ["Initial Consultation", "£500.00", "1", "£500.00", "20%", "£600.00"],
        ["Live Server set up", "£800.00", "1", "£800.00", "20%", "£960.00"],
    ]

    # Define each column width as a fraction of doc.width
    col_widths = [
        doc.width * 0.30,  # Description 30%
        doc.width * 0.15,  # Unit Price 15%
        doc.width * 0.10,  # Qty 10%
        doc.width * 0.15,  # Net 15%
        doc.width * 0.10,  # VAT 10%
        doc.width * 0.20   # Gross 20%
    ]

    items_table = Table(items_data, colWidths=col_widths)
    items_table.setStyle(TableStyle([
        # Darker blue header
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#003366")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        # Horizontal lines only (no vertical borders)
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.white),
        ('LINEBELOW', (0, 1), (-1, -1), 0.25, colors.grey),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
    ]))
    story.append(items_table)

    # -- Totals Table --
    totals_data = [
        ["", ""],
        ["Net Total", "£2600.00"],
        ["VAT", "£520.00"],
        ["Gross", "£3120.00"]
    ]
    totals_table = Table(totals_data, colWidths=[4*cm, 3*cm])
    totals_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (0, 0), (1, -1), 'CENTER'),
        ('BACKGROUND', (0, 1), (0, -1), colors.HexColor("#003366")),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.grey),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))

    # -- Due Note --
    due_note = Paragraph(
        "This invoice is due within 30 days", styles['DueNote'])

    # -- Combine Totals Table and Due Note Side by Side --
    # We'll use a container table with 2 columns, each taking half of the available width.
    combined_table = Table([[due_note, totals_table]],
                           colWidths=[doc.width/2, doc.width/2])
    combined_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(Spacer(1, 12))
    story.append(combined_table)

    # Build the PDF
    doc.build(story)
    print(f"Invoice '{filename}' created successfully!")


if __name__ == "__main__":
    create_invoice("improved_invoice.pdf")
