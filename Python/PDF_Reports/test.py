from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Frame, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def create_pdf(filename):
    c = canvas.Canvas(filename, pagesize=A4)

    width, height = A4  # Get page dimensions

    # Define a frame (x, y, width, height)
    frame_x = inch
    frame_y = inch

    frame_width = width - 2 * inch  # Leave 1 inch margin on left & right

    frame_height = height - 2 * inch  # Leave 1 inch margin on top & bottom

    frame = Frame(frame_x, frame_y, frame_width,
                  frame_height, showBoundary=True)

    # Sample text as a Paragraph
    styles = getSampleStyleSheet()
    story = [
        Paragraph("This is a paragraph inside the frame.", styles["Normal"])]

    # Add content to the frame
    frame.addFromList(story, c)

    # Save the canvas
    c.save()


def create_pdf(filename):
    c = canvas.Canvas(filename, pagesize=landscape(A4))  # Set landscape mode
    width, height = landscape(A4)  # Get new page dimensions

    # Define a frame with 1-inch margins
    frame_x = inch
    frame_y = inch
    frame_width = width - 2 * inch
    frame_height = height - 2 * inch

    frame = Frame(frame_x, frame_y, frame_width,
                  frame_height)

    # Sample text
    styles = getSampleStyleSheet()
    story = [Paragraph(
        "This is a paragraph inside the frame on a landscape page.", styles["Normal"])]

    # Add content to the frame
    frame.addFromList(story, c)

    # Save the PDF
    c.save()


# Generate the PDF in landscape mode
create_pdf("landscape_document.pdf")
