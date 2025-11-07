import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime
from plyer import notification
import winsound
import json
import os
import threading
import time
import ollama

REMINDER_FILE = "reminders.json"

# Medication options and risks
medication_risks = {
    "Paracetamol": "Overuse may cause liver damage.",
    "Cetirizine": "May cause drowsiness or dry mouth.",
    "Dextromethorphan": "Overdose can lead to confusion or dizziness.",
    "Losartan": "Can cause dizziness or increased potassium levels.",
    "Amlodipine": "May cause swelling or fatigue.",
    "Levocetirizine": "Can cause drowsiness and dry throat.",
    "Chlorpheniramine": "May cause sedation or blurred vision."
}

# Load and save reminders
def load_reminders():
    if os.path.exists(REMINDER_FILE):
        with open(REMINDER_FILE, "r") as f:
            data = json.load(f)
            for date in data:
                data[date] = [
                    {"time": "09:00", "text": r, "medication": "", "risk": ""} if isinstance(r, str) else r
                    for r in data[date]
                ]
            return data
    else:
        today = datetime.now().strftime("%d/%m/%Y")
        sample = {
            today: [
                {"time": "16:45", "text": "Take Paracetamol", "medication": "Paracetamol", "risk": medication_risks["Paracetamol"]},
                {"time": "16:46", "text": "Take Cetirizine", "medication": "Cetirizine", "risk": medication_risks["Cetirizine"]}
            ]
        }
        save_reminders(sample)
        return sample

def save_reminders(reminders):
    with open(REMINDER_FILE, "w") as f:
        json.dump(reminders, f)

reminders = load_reminders()

# GUI setup
root = tk.Tk()
root.title("AI Calendar Reminder")
root.geometry("800x700")
root.configure(bg="#f0f0f0")

style = ttk.Style(root)
style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.configure("TLabel", font=("Segoe UI", 11))

# Calendar widget
cal_frame = tk.Frame(root)
cal_frame.pack(pady=10)

cal = Calendar(cal_frame, selectmode='day', date_pattern='dd/mm/yyyy')
cal.pack()

selected_date = cal.get_date()

# Reminder display
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
            reminder_text = ttk.Label(frame, text=f"{idx + 1}. {reminder['time']} - {reminder['text']}{med}{risk}", font=("Segoe UI", 11))
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

# Add reminder section with dropdowns
add_frame = tk.Frame(root, bg="#f0f0f0")
add_frame.pack(pady=20)

reminder_entry = ttk.Entry(add_frame, width=30)
reminder_entry.pack(side=tk.LEFT, padx=5)

time_entry = ttk.Entry(add_frame, width=10)
time_entry.pack(side=tk.LEFT, padx=5)
time_entry.insert(0, "HH:MM")

med_var = tk.StringVar()
med_dropdown = ttk.Combobox(add_frame, textvariable=med_var, width=20)
med_dropdown['values'] = list(medication_risks.keys())
med_dropdown.set("Select Medication")
med_dropdown.pack(side=tk.LEFT, padx=5)

risk_var = tk.StringVar()
risk_dropdown = ttk.Combobox(add_frame, textvariable=risk_var, width=40)
risk_dropdown.set("Select Risk")
risk_dropdown.pack(side=tk.LEFT, padx=5)

def update_risk_dropdown(event):
    selected_med = med_var.get()
    risk = medication_risks.get(selected_med, "")
    risk_var.set(risk)

med_dropdown.bind("<<ComboboxSelected>>", update_risk_dropdown)

def add_reminder():
    #note = reminder_entry.get().strip()
    time_str = time_entry.get().strip()
    med = med_var.get().strip()
    risk = risk_var.get().strip()
    if not note or not time_str or med == "Select Medication" or not risk:
        messagebox.showwarning("Empty", "Please enter reminder, time, and select medication with risk.")
        return

    new_entry = {"time": time_str, "text": note, "medication": med, "risk": risk}
    if selected_date in reminders:
        reminders[selected_date].append(new_entry)
    else:
        reminders[selected_date] = [new_entry]
    save_reminders(reminders)
    refresh_calendar_tags()
    refresh_reminders()
    reminder_entry.delete(0, tk.END)
    time_entry.delete(0, tk.END)
    med_dropdown.set("Select Medication")
    risk_dropdown.set("Select Risk")

add_btn = ttk.Button(add_frame, text="Add Reminder", command=add_reminder)
add_btn.pack(side=tk.LEFT, padx=5)

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

# AI reminder checker
def check_ai_reminders():
    now = datetime.now()
    date_str = now.strftime("%d/%m/%Y")
    time_str = now.strftime("%H:%M")

    if date_str in reminders:
        for reminder in reminders[date_str]:
            if reminder["time"] == time_str:
                prompt = f"Send a friendly reminder to the user: '{reminder['text']}'. Also mention any health risks: '{reminder['risk']}'"

                try:
                    response = ollama.chat(model='llama2', messages=[{"role": "user", "content": prompt}])
                    message = response['message']['content']
                except:
                    message = f"{reminder['text']}\nRisk: {reminder['risk']}" if reminder['risk'] else reminder['text']

                notification.notify(title="🤖 AI Reminder", message=message, timeout=5)
                winsound.MessageBeep(winsound.MB_ICONASTERISK)

def background_loop():
    while True:
        check_ai_reminders()
        time.sleep(60)

threading.Thread(target=background_loop, daemon=True).start()

# Init
refresh_calendar_tags()
refresh_reminders()
root.mainloop()
