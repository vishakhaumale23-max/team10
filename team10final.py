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

# Medication options with risks and benefits
medication_info = {
    "Paracetamol": {"risk": "Overuse may cause liver damage.", "benefit": "Reduces fever and mild pain."},
    "Cetirizine": {"risk": "May cause drowsiness or dry mouth.", "benefit": "Relieves allergy symptoms."},
    "Dextromethorphan": {"risk": "Overdose can lead to confusion or dizziness.", "benefit": "Suppresses cough."},
    "Losartan": {"risk": "Can cause dizziness or increased potassium levels.", "benefit": "Lowers blood pressure."},
    "Amlodipine": {"risk": "May cause swelling or fatigue.", "benefit": "Treats hypertension and angina."},
    "Levocetirizine": {"risk": "Can cause drowsiness and dry throat.", "benefit": "Relieves allergy symptoms."},
    "Chlorpheniramine": {"risk": "May cause sedation or blurred vision.", "benefit": "Relieves cold and allergy symptoms."},
    "Ibuprofen": {"risk": "May cause stomach ulcers or kidney issues.", "benefit": "Reduces inflammation and pain."},
    "Metformin": {"risk": "May lead to lactic acidosis in rare cases.", "benefit": "Controls blood sugar in type 2 diabetes."},
    "Atorvastatin": {"risk": "May cause muscle pain or liver enzyme elevation.", "benefit": "Lowers cholesterol."},
    "Omeprazole": {"risk": "May cause headache or nutrient malabsorption.", "benefit": "Reduces stomach acid."},
    "Amoxicillin": {"risk": "May cause allergic reactions or diarrhea.", "benefit": "Treats bacterial infections."},
    "Hydrochlorothiazide": {"risk": "May cause dehydration or electrolyte imbalance.", "benefit": "Lowers blood pressure."},
    "Clopidogrel": {"risk": "May increase bleeding risk.", "benefit": "Prevents blood clots."},
    "Vitamin D": {"risk": "Excess intake may lead to calcium buildup in the blood.", "benefit": "Supports bone health."},
    "Calcium Carbonate": {"risk": "Too much can cause kidney stones or constipation.", "benefit": "Strengthens bones."},
    "Zinc Sulfate": {"risk": "May cause nausea or metallic taste.", "benefit": "Boosts immunity."},
    "Iron (Ferrous Sulfate)": {"risk": "May cause constipation or dark stools.", "benefit": "Treats iron deficiency anemia."},
    "Probiotic Capsules": {"risk": "May cause bloating or gas.", "benefit": "Supports gut health."},
    "Aspirin": {"risk": "Risk of bleeding, especially with other blood thinners.", "benefit": "Relieves pain and reduces clotting."}
}

# Load and save reminders
def load_reminders():
    if os.path.exists(REMINDER_FILE):
        with open(REMINDER_FILE, "r") as f:
            return json.load(f)
    today = datetime.now().strftime("%d/%m/%Y")
    sample = {
        today: [{
            "time": "17:20",
            "text": "Take Paracetamol",
            "medication": "Paracetamol",
            "risk": medication_info["Paracetamol"]["risk"],
            "benefit": medication_info["Paracetamol"]["benefit"]
        }]
    }
    save_reminders(sample)
    return sample

def save_reminders(data):
    with open(REMINDER_FILE, "w") as f:
        json.dump(data, f)

reminders = load_reminders()

# GUI setup
root = tk.Tk()
root.title("AI Medication Reminder")
root.geometry("850x700")
root.configure(bg="#f0f0f0")

style = ttk.Style(root)
style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.configure("TLabel", font=("Segoe UI", 11))

cal_frame = tk.Frame(root)
cal_frame.pack(pady=10)

cal = Calendar(cal_frame, selectmode='day', date_pattern='dd/mm/yyyy')
cal.pack()

selected_date = cal.get_date()

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

# Add reminder section
add_frame = tk.Frame(root, bg="#f0f0f0")
add_frame.pack(pady=20)

reminder_entry = ttk.Entry(add_frame, width=30)
reminder_entry.insert(0, "Take your medication")
reminder_entry.pack(side=tk.LEFT, padx=5)

time_entry = ttk.Entry(add_frame, width=10)
time_entry.insert(0, "HH:MM")
time_entry.pack(side=tk.LEFT, padx=5)

med_var = tk.StringVar()
med_dropdown = ttk.Combobox(add_frame, textvariable=med_var, width=20)
med_dropdown['values'] = list(medication_info.keys())
med_dropdown.set("Paracetamol")
med_dropdown.pack(side=tk.LEFT, padx=5)

risk_var = tk.StringVar()
risk_dropdown = ttk.Combobox(add_frame, textvariable=risk_var, width=40)
risk_dropdown.set(medication_info["Paracetamol"]["risk"])
risk_dropdown.pack(side=tk.LEFT, padx=5)

benefit_var = tk.StringVar()
benefit_dropdown = ttk.Combobox(add_frame, textvariable=benefit_var, width=40)
benefit_dropdown.set(medication_info["Paracetamol"]["benefit"])
benefit_dropdown.pack(side=tk.LEFT, padx=5)

def update_info_dropdown(event):
    med = med_var.get()
    risk_var.set(medication_info[med]["risk"])
    benefit_var.set(medication_info[med]["benefit"])

med_dropdown.bind("<<ComboboxSelected>>", update_info_dropdown)

def add_reminder():
    note = reminder_entry.get().strip()
    time_str = time_entry.get().strip()
    med = med_var.get().strip()
    risk = risk_var.get().strip()
    benefit = benefit_var.get().strip()
    if not note or not time_str or not med or not risk or not benefit:
        messagebox.showwarning("Empty", "Please fill all fields.")
        return
    new_entry = {"time": time_str, "text": note, "medication": med, "risk": risk, "benefit": benefit}
    if selected_date in reminders:
        reminders[selected_date].append(new_entry)
    else:
        reminders[selected_date] = [new_entry]
    save_reminders(reminders)
    refresh_calendar_tags()
    refresh_reminders()
    reminder_entry.delete(0, tk.END)
    reminder_entry.insert(0, "Take your medication")
    time_entry.delete(0, tk.END)
    time_entry.insert(0, "HH:MM")
    med_dropdown.set("Paracetamol")
    risk_dropdown.set(medication_info["    risk"])
    benefit_dropdown.set(medication_info["Paracetamol"]["benefit"])

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
                med_name = reminder.get("medication", "")
                risk = reminder.get("risk", "")
                benefit = reminder.get("benefit", "")
                prompt = (
                    f"Send a friendly reminder to take '{med_name}'. "
                    f"Reminder text: '{reminder['text']}'. "
                    f"Include health risk: '{risk}' and benefit: '{benefit}'."
                )

                try:
                    response = ollama.chat(model='llama2', messages=[{"role": "user", "content": prompt}])
                    message = response['message']['content']
                except:
                    message = f"Time to take {med_name}.\n{reminder['text']}\nBenefit: {benefit}\nRisk: {risk}"

                notification.notify(
                    title=f"💊 Reminder: {med_name}",
                    message=message,
                    timeout=5
                )
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
