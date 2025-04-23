import os
import datetime
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image,
    PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# Output path
output_pdf_path = "reportlab_full_analysis_v3_improved.pdf"

# Image paths
image_heatmap = "chandigarh_customer_heatmap.png"
image_iterations_analysis = "iterations_analysis_dense_grid.png"
image_routes = "chandigarh_routes_map.jpg"
image_time_compare = "time_compare.png"
image_time_table = "DistanceTable.png"
image_delivery = "delivery.png"
image_delivery_stats = "deliverystats.jpg"

# Text for Iterations section
iterations_text = ("The number of iterations of ABC can have a significant impact on the "
                   "efficiency of the path that has been calculated by the algorithm.")

# Timestamp
generation_time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Document Setup
doc = SimpleDocTemplate(output_pdf_path, pagesize=letter,
                        rightMargin=inch, leftMargin=inch,
                        topMargin=inch, bottomMargin=inch)
styles = getSampleStyleSheet()

# Custom styles
styles.add(ParagraphStyle(name='h3_custom',
                          parent=styles['Heading3'],
                          fontSize=12))

# Story
story = []

available_width = doc.width

# Header for timestamp
def add_page_header(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawRightString(doc.pagesize[0] - doc.rightMargin,
                           doc.pagesize[1] - 0.75 * inch,
                           f"Generated: {generation_time_str}")
    canvas.restoreState()

# Add image with optional caption
def add_image_to_story(img_file, story_list, width, caption=None):
    if not os.path.exists(img_file):
        print(f"Warning: Image file not found, skipping: {img_file}")
        story_list.append(Paragraph(f"<para color='red'>Error: Image file '{img_file}' not found.</para>", styles['Normal']))

        return False
    try:
        img = Image(img_file, width=width, height=None)
        img.drawHeight = width * img.imageHeight / img.imageWidth
        img.drawWidth = width
        story_list.append(img)
        if caption:
            story_list.append(Spacer(1, 0.1 * inch))
            story_list.append(Paragraph(f"<i>{caption}</i>", styles['Italic']))
        return True
    except Exception as e:
        print(f"Error processing image {img_file}: {e}")
        return False


# 1. Artificial Bee Colony Algorithm
story.append(Paragraph("Artificial Bee Colony Algorithm", styles['Heading1']))
story.append(Spacer(1, 0.3 * inch))

# 2. Customer Distribution
story.append(Paragraph("Customer Distribution", styles['Heading2']))

add_image_to_story(image_heatmap, story, available_width, "Figure 1: Heatmap of Customer Distribution")
story.append(PageBreak())
# 3. Iterations ABC
story.append(Paragraph("Iterations ABC", styles['h3_custom']))
add_image_to_story(image_iterations_analysis, story, available_width, "Figure 2: Iteration Impact on Route Efficiency")
story.append(Paragraph(iterations_text, styles['Normal']))
story.append(Spacer(1, 0.3 * inch))
story.append(PageBreak())
# 4. Routes ABC
story.append(Paragraph("Routes ABC", styles['Heading2']))

add_image_to_story(image_routes, story, available_width, "Figure 3: Optimal Routes from ABC Algorithm")
story.append(Paragraph("Optimal routes that have been calculated by the algorithm", styles['Normal']))
story.append(PageBreak())
# 5. Comparing Algorithms
story.append(Paragraph("Comparing Algorithms", styles['Heading2']))
story.append(Spacer(1, 0.1 * inch))
add_image_to_story(image_time_compare, story, available_width, "Figure 4: Time Comparison Across Algorithms")
add_image_to_story(image_time_table, story, available_width, "Figure 5: Distance and Time Table")
story.append(PageBreak())
# 6. Delivery Schedule
story.append(Paragraph("Delivery Schedule", styles['Heading2']))
story.append(Spacer(1, 0.1 * inch))
add_image_to_story(image_delivery, story, available_width, "Figure 6: Delivery Timeline Chart")
add_image_to_story(image_delivery_stats, story, available_width, "Figure 7: Statistical Distribution of Deliveries")

# 7. Conclusion
story.append(PageBreak())
story.append(Paragraph("Conclusion", styles['Heading2']))
story.append(Spacer(1, 0.1 * inch))
story.append(Paragraph(
    "The Artificial Bee Colony algorithm proves to be an effective method for optimizing delivery routes in urban spaces. "
    "The results suggest that increasing iteration count yields better efficiency, but there is a trade-off with computation time. "
    "Future work can involve integrating real-time traffic data and hybridizing with other swarm-based methods.",
    styles['Normal']))
story.append(Spacer(1, 0.2 * inch))

# --- GENERATE PDF ---
try:
    doc.build(story, onFirstPage=add_page_header, onLaterPages=add_page_header)
    print(f"Successfully created PDF: {output_pdf_path}")
except Exception as e:
    print(f"An error occurred during PDF building: {e}")
