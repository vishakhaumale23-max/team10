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
selected_date = datetime.now().strftime("%d/%m/%Y")

def scan_prescription(image_path):
    text = pytesseract.image_to_string(Image.open(image_path)).lower()
    extracted = []
    for med in medication_info:
        if med.lower() in text:
            if "every 6 hours" in text:
                times = ["06:00", "12:00", "18:00", "00:00"]
            elif "twice daily" in text:
                times = ["08:00", "20:00"]
            elif "at night" in text:
                times = ["21:00"]
            else:
                times = ["09:00"]
            extracted.append((med, times))
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
    refresh_calendar_tags()
    refresh_reminders()

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

# GUI Setup
root = tk.Tk()
root.title("AI Prescription Reminder with Ollama")
root.geometry("800x600")
root.configure(bg="#f0f0f0")

cal = Calendar(root, selectmode='day', date_pattern='dd/mm/yyyy')
cal.pack(pady=10)

reminder_list_frame = tk.Frame(root, bg="#f0f0f0")
reminder_list_frame.pack(pady=10)

reminder_label = ttk.Label(reminder_list_frame, text=f"Reminders for {selected_date}:", font=("Segoe UI", 12, "bold"))
reminder_label.pack()

reminder_container = tk.Frame(reminder_list_frame, bg="#f0f0f0")
reminder_container.pack()

def refresh_reminders():
    for widget in reminder_container.winfo_children():
        widget.destroy()
    reminder_label.config(text=f"Reminders for {selected_date}:")
    if selected_date in reminders:
        for idx, reminder in enumerate(reminders[selected_date]):
            frame = tk.Frame(reminder_container, bg="#f0f0f0")
            frame.pack(anchor='w', pady=2)
            med = f" ({reminder['medication']})" if reminder.get("medication") else ""
            risk = f" - Risk: {reminder['risk']}" if reminder.get("risk") else ""
            benefit = f" - Benefit: {reminder['benefit']}" if reminder.get("benefit") else ""
            reminder_text = ttk.Label(frame, text=f"{idx + 1}. {reminder['time']} - {reminder['text']}{med}{risk}{benefit}", font=("Segoe UI", 11))
            reminder_text.pack(side=tk.LEFT, padx=5)
            delete_btn = ttk.Button(frame, text="Delete", command=lambda i=idx: delete_reminder(i))
            delete_btn.pack(side=tk.LEFT, padx=5)

def delete_reminder(index):
    reminders[selected_date].pop(index)
    if not reminders[selected_date]:
        reminders.pop(selected_date)
    save_reminders(reminders)
    refresh_calendar_tags()
    refresh_reminders()

def on_date_click(event):
    global selected_date
    selected_date = cal.get_date()
    refresh_reminders()

cal.bind("<<CalendarSelected>>", on_date_click)

def refresh_calendar_tags():
    cal.calevent_remove('all')
    for date_str in reminders:
        try:
            dt = datetime.strptime(date_str, "%d/%m/%Y")
            cal.calevent_create(dt, "📌", "reminder")
        except:
            pass
    cal.tag_config("reminder", background="#fdf2dc", foreground="black")

def upload_and_process():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
    if not file_path:
        return
    meds = scan_prescription(file_path)
    if not meds:
        messagebox.showwarning("No Medications Found", "Could not extract known medications from the image.")
        return
    date = cal.get_date()
    add_prescription_to_reminders(date, meds)
    messagebox.showinfo("Success", f"Reminders added for {date}:\n" + "\n".join([f"{m[0]} at {', '.join(m[1])}" for m in meds]))

upload_btn = ttk.Button(root, text="Upload Prescription Image", command=upload_and_process)
upload_btn.pack(pady=20)

refresh_calendar_tags()
refresh_reminders()
root.mainloop()
