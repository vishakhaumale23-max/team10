# notifications.py

def send_medication_notification(patient_name, medication_list, email):
    subject = f"Medication Reminder for {patient_name}"
    medications = "\n".join(f"- {med}" for med in medication_list)
    message = f"""Dear {patient_name},

This is a reminder to take your medications as prescribed:

{medications}

If you have any questions, please contact your healthcare provider.

Best regards,
Your Healthcare Team
"""
    # Placeholder for sending email logic
    print(f"Sending email to: {email}")
    print(f"Subject: {subject}")
    print(message)

# Example usage:
patients = [
    {
        "name": "Rina Umale",
        "medications": ["Aspirin 75mg", "Metformin 500mg"],
        "email": "rina.umale@example.com"
    },
    {
        "name": "Ravindra Umale",
        "medications": ["Atorvastatin 10mg", "Lisinopril 20mg"],
        "email": "ravindra.umale@example.com"
    }
]

for patient in patients:
    send_medication_notification(patient["name"], patient["medications"], patient["email"])