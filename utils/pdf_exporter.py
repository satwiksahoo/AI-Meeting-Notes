# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib import colors
# import io

# def create_summary_pdf(summary: dict) -> bytes:
#     buffer = io.BytesIO()
#     doc = SimpleDocTemplate(buffer)
#     styles = getSampleStyleSheet()
#     story = []

#     # Title
#     story.append(Paragraph("Meeting Summary", styles['Title']))
#     story.append(Spacer(1, 12))

#     # Key Points
#     story.append(Paragraph("Key Points", styles['Heading2']))
#     for kp in summary.get("key_points", []):
#         story.append(Paragraph(f"• {kp}", styles['Normal']))
#     story.append(Spacer(1, 12))

#     # Decisions
#     story.append(Paragraph("Decisions", styles['Heading2']))
#     for d in summary.get("decisions", []):
#         story.append(Paragraph(f"• {d}", styles['Normal']))
#     story.append(Spacer(1, 12))

#     # Action Items
#     # Action Items
#     story.append(Paragraph("Action Items", styles['Heading2']))
#     action_items = summary.get("action_items", [])
#     if action_items:
#         table_data = [["Owner", "Task", "Due Date", "Priority"]]
#         for ai in action_items:
#             if isinstance(ai, dict):  # expected case
#                 table_data.append([
#                     ai.get("owner", ""),
#                     ai.get("task", ""),
#                     ai.get("due_date", ""),
#                     ai.get("priority", "")
#                 ])
#             else:  # fallback if it's just a string
#                 table_data.append(["", str(ai), "", ""])
#         table = Table(table_data, colWidths=[100, 250, 80, 60])
#         table.setStyle(TableStyle([
#             ('BACKGROUND', (0,0), (-1,0), colors.grey),
#             ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
#             ('ALIGN', (0,0), (-1,-1), 'LEFT'),
#             ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
#             ('BOTTOMPADDING', (0,0), (-1,0), 8),
#             ('BACKGROUND', (0,1), (-1,-1), colors.beige),
#             ('GRID', (0,0), (-1,-1), 1, colors.black),
#         ]))
#         story.append(table)



#     doc.build(story)
#     pdf = buffer.getvalue()
#     buffer.close()
#     return pdf


from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
import io
from datetime import datetime

def create_summary_pdf(summary: dict) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40, leftMargin=40,
        topMargin=50, bottomMargin=40
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="SectionHeader", fontSize=14, leading=16, spaceAfter=10, textColor=colors.HexColor("#2C3E50"), fontName="Helvetica-Bold"))
    styles.add(ParagraphStyle(name="NormalText", fontSize=11, leading=14, spaceAfter=6))

    story = []

    # Title + Date
    story.append(Paragraph("📄 Meeting Summary Report", styles['Title']))
    story.append(Paragraph(datetime.now().strftime("%B %d, %Y"), styles['Normal']))
    story.append(Spacer(1, 20))

    # --- Key Points ---
    story.append(Paragraph("Key Points", styles['SectionHeader']))
    key_points = summary.get("key_points", [])
    if key_points:
        table_data = [[f"{i+1}.", kp] for i, kp in enumerate(key_points)]
        table = Table(table_data, colWidths=[20, 450])
        table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.grey),
            ('BOX', (0,0), (-1,-1), 0.25, colors.grey),
        ]))
        story.append(table)
    story.append(Spacer(1, 15))

    # --- Decisions ---
    story.append(Paragraph("Decisions", styles['SectionHeader']))
    decisions = summary.get("decisions", [])
    if decisions:
        table_data = [[f"{i+1}.", d] for i, d in enumerate(decisions)]
        table = Table(table_data, colWidths=[20, 450])
        table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.grey),
            ('BOX', (0,0), (-1,-1), 0.25, colors.grey),
        ]))
        story.append(table)
    story.append(Spacer(1, 15))

    # --- Action Items ---
    story.append(Paragraph("Action Items", styles['SectionHeader']))
    action_items = summary.get("action_items", [])
    if action_items:
        table_data = [["Owner", "Task", "Due Date", "Priority"]]
        for ai in action_items:
            if isinstance(ai, dict):
                table_data.append([
                    ai.get("owner", ""),
                    ai.get("task", ""),
                    ai.get("due_date", ""),
                    ai.get("priority", "")
                ])
            else:
                table_data.append(["", str(ai), "", ""])
        table = Table(table_data, colWidths=[100, 250, 80, 60])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2C3E50")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,0), 8),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ]))
        story.append(table)

    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
