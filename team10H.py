import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkcalendar import Calendar
from datetime import datetime
from plyer import notification
import pytesseract
from PIL import Image
import json
import threading
import time
import ollama

REMINDER_FILE = "reminders.json"

medication_info = {
    "Paracetamol": {"risk": "Overuse may cause liver damage.", "benefit": "Reduces fever and mild pain."},
    "Cetirizine": {"risk": "May cause drowsiness or dry mouth.", "benefit": "Relieves allergy symptoms."},
    "Dextromethorphan": {"risk": "Overdose can lead to confusion or dizziness.", "benefit": "Suppresses cough."}
}

def load_reminders():
    try:
        with open(REMINDER_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_reminders(data):
    with open(REMINDER_FILE, "w") as f:
        json.dump(data, f)

reminders = load_reminders()

def scan_prescription(image_path):
    text = pytesseract.image_to_string(Image.open(image_path))
    extracted = []
    lines = text.split("\n")
    for line in lines:
        if "Paracetamol" in line:
            extracted.append(("Paracetamol", ["06:00", "12:00", "18:00", "00:00"]))
        elif "Cetirizine" in line:
            extracted.append(("Cetirizine", ["21:00"]))
        elif "Dextromethorphan" in line:
            extracted.append(("Dextromethorphan", ["08:00", "20:00"]))
    return extracted

def add_prescription_to_reminders(date, meds):
    for med, times in meds:
        for t in times:
            reminders.setdefault(date, []).append({
                "time": t,
                "text": f"Take {med}",
                "medication": med,
                "risk": medication_info[med]["risk"],
                "benefit": medication_info[med]["benefit"]
            })
    save_reminders(reminders)

def generate_ai_message(reminder):
    prompt = (
        f"Send a friendly reminder to take '{reminder['medication']}'. "
        f"Reminder text: '{reminder['text']}'. "
        f"Include health risk: '{reminder['risk']}' and benefit: '{reminder['benefit']}'."
    )
    try:
        response = ollama.chat(model='llama2', messages=[{"role": "user", "content": prompt}])
        return response['message']['content'].strip()
    except:
        return f"Time to take {reminder['medication']}.\nBenefit: {reminder['benefit']}\nRisk: {reminder['risk']}"

def check_reminders():
    now = datetime.now()
    date_str = now.strftime("%d/%m/%Y")
    time_str = now.strftime("%H:%M")
    if date_str in reminders:
        for reminder in reminders[date_str]:
            if reminder["time"] == time_str:
                msg = generate_ai_message(reminder)
                notification.notify(
                    title=f"💊 Reminder: {reminder['medication']}",
                    message=msg,
                    timeout=5
                )

def background_loop():
    while True:
        check_reminders()
        time.sleep(60)

threading.Thread(target=background_loop, daemon=True).start()

# GUI
root = tk.Tk()
root.title("AI Prescription Reminder with Ollama")
root.geometry("600x400")

cal = Calendar(root, selectmode='day', date_pattern='dd/mm/yyyy')
cal.pack(pady=10)

def upload_and_process():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
    if not file_path:
        return
    meds = scan_prescription(file_path)
    date = cal.get_date()
    add_prescription_to_reminders(date, meds)
    messagebox.showinfo("Success", f"Reminders added for {date}!")

upload_btn = ttk.Button(root, text="Upload Prescription Image", command=upload_and_process)
upload_btn.pack(pady=20)

root.mainloop()
