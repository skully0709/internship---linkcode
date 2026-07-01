import smtplib
from email.message import EmailMessage

def send_email(receiver_email, pdf_file):

    sender_email = "mydemoemail9@gmail.com"
    app_password = "qwrhustvqisvspqh"

    msg = EmailMessage()

    msg["Subject"] = "Student Report Card"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    msg.set_content(
        "Please find the attached student report card."
    )

    with open(pdf_file, "rb") as f:
        file_data = f.read()

    msg.add_attachment(
        file_data,
        maintype="application",
        subtype="pdf",
        filename=pdf_file
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, app_password)
        smtp.send_message(msg)

    print("Email sent successfully!")
