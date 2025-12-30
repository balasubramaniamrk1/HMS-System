from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO

def generate_prescription_pdf(consultation):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Hospital Header
    header_style = ParagraphStyle(
        'Header',
        parent=styles['Heading1'],
        alignment=1, # Center
        spaceAfter=20
    )
    elements.append(Paragraph("Hospital Management System", header_style))
    elements.append(Spacer(1, 12))

    # Doctor and Patient Details
    doctor = consultation.appointment.doctor
    patient_name = consultation.appointment.name
    date = consultation.consultation_date.date()
    
    # Safe Extraction of Doctor Details
    if doctor:
        doc_name = f"Dr. {doctor.name}"
        doc_qual = doctor.qualifications
        doc_spec = doctor.specialization
    else:
        # Fallback if no doctor assigned (e.g. Department only)
        dept_name = consultation.appointment.department.name if consultation.appointment.department else "General"
        doc_name = "Medical Officer"
        doc_qual = dept_name
        doc_spec = "Hospital Staff"

    data = [
        [doc_name, f"Date: {date}"],
        [doc_qual, f"Patient: {patient_name}"],
        [doc_spec, f"ID: {consultation.appointment.id}"]
    ]
    
    t = Table(data, colWidths=[300, 200])
    t.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Rx", styles['Heading2']))

    # Medicines Table
    medicines_data = [['Medicine', 'Dosage', 'Duration', 'Instructions']]
    for item in consultation.prescription_items.all():
        medicines_data.append([
            item.medicine_name,
            item.dosage,
            item.duration,
            item.instruction
        ])

    t2 = Table(medicines_data, colWidths=[200, 100, 100, 150])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(t2)
    
    elements.append(Spacer(1, 20))
    
    # Diagnosis and Notes
    elements.append(Paragraph(f"<b>Diagnosis:</b> {consultation.diagnosis}", styles['Normal']))
    if consultation.next_visit_date:
        elements.append(Paragraph(f"<b>Next Visit:</b> {consultation.next_visit_date}", styles['Normal']))
        
    elements.append(Spacer(1, 40))
    elements.append(Paragraph("_______________________", styles['Normal']))
    elements.append(Paragraph("Doctor's Signature", styles['Normal']))

    doc.build(elements)
    buffer.seek(0)
    return buffer
