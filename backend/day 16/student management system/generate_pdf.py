from fpdf import FPDF

def generate_pdf(row, total, percentage, result):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="STUDENT REPORT CARD", ln=True, align="C")

    pdf.ln(10)

    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt=f"Roll No : {row[0]}", ln=True)
    pdf.cell(200, 10, txt=f"Name : {row[1]}", ln=True)
    pdf.cell(200, 10, txt=f"Age : {row[2]}", ln=True)

    pdf.ln(5)

    pdf.cell(200, 10, txt=f"Marathi Marks : {row[3]}", ln=True)
    pdf.cell(200, 10, txt=f"English Marks : {row[4]}", ln=True)
    pdf.cell(200, 10, txt=f"Maths Marks : {row[5]}", ln=True)
    pdf.cell(200, 10, txt=f"Science Marks : {row[6]}", ln=True)
    pdf.cell(200, 10, txt=f"Economics Marks : {row[7]}", ln=True)

    pdf.ln(5)

    pdf.cell(200, 10, txt=f"Total Marks : {total}/500", ln=True)
    pdf.cell(200, 10, txt=f"Percentage : {percentage:.2f}%", ln=True)
    pdf.cell(200, 10, txt=f"Result : {result}", ln=True)

    filename = f"report_{row[0]}.pdf"

    pdf.output(filename)

    print(f"PDF generated successfully: {filename}")
