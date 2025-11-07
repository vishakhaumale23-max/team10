import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import schedule
import time

# Patient data
patients = [
    {"name": "Rina Umale", "age": 52, "email": "shashanktripathi1703@gmail.com"},
    {"name": "Ravindra Umale", "age": 53, "email": "shashanktripathi1703@gmail.com"}
]

# Email credentials and settings
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "shashanktripathi@1703gmail.com"
EMAIL_PASSWORD = "osfl ywvs yeub tklc"  # Use app password for Gmail

def send_medication_reminder(patient):
    subject = "Medication Reminder"
    body = (
        f"Dear {patient['name']},\n\n"
        "This is a reminder to take your medication as scheduled.\n"
        "Please also be aware of potential drug interactions. "
        "If you have any questions, consult your healthcare provider.\n\n"
        "Stay healthy!\n"
    )
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = patient["email"]

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, patient["email"], msg.as_string())
        print(f"Reminder sent to {patient['name']} at {datetime.now()}")
    except Exception as e:
        print(f"Failed to send email to {patient['name']}: {e}")

def send_reminders():
    for patient in patients:
        send_medication_reminder(patient)

# Schedule reminders at 9:00 AM and 2:36 PM
schedule.every().day.at("09:00").do(send_reminders)
schedule.every().day.at("14:55").do(send_reminders)

if __name__ == "__main__":
    print("Medication reminder service started.")
    while True:
        schedule.run_pending()
        time.sleep(60)