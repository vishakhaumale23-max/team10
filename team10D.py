# import tkinter as tk
# from tkinter import ttk, messagebox
# from tkcalendar import Calendar
# from datetime import datetime
# from plyer import notification
# import winsound
# import json
# import os
# import threading
# import time
# import ollama

# REMINDER_FILE = "reminders.json"

# # Medication options with risks and benefits
# medication_info = {
#     "Paracetamol": {
#         "risk": "Overuse may cause liver damage.",
#         "benefit": "Reduces fever and mild pain."
#     },
#     "Ibuprofen": {
#         "risk": "Stomach ulcers, kidney issues.",
#         "benefit": "Anti-inflammatory, relieves pain."
#     },
#     "Cetirizine": {
#         "risk": "Drowsiness, dry mouth.",
#         "benefit": "Treats allergies and hay fever."
#     },
#     "Dextromethorphan": {
#         "risk": "Dizziness, confusion in high doses.",
#         "benefit": "Suppresses cough."
#     },
#     "Losartan": {
#         "risk": "Dizziness, increased potassium.",
#         "benefit": "Controls high blood pressure."
#     },
#     "Amlodipine": {
#         "risk": "Swelling, fatigue.",
#         "benefit": "Treats hypertension and angina."
#     },
#     "Levocetirizine": {
#         "risk": "Drowsiness, dry throat.",
#         "benefit": "Allergy relief."
#     },
#     "Chlorpheniramine": {
#         "risk": "Sedation, blurred vision.",
#         "benefit": "Cold and allergy relief."
#     },
#     "Metformin": {
#         "risk": "Lactic acidosis (rare), GI upset.",
#         "benefit": "Controls blood sugar in type 2 diabetes."
#     },
#     "Atorvastatin": {
#         "risk": "Muscle pain, liver enzyme elevation.",
#         "benefit": "Lowers cholesterol."
#     },
#     "Omeprazole": {
#         "risk": "Headache, nutrient malabsorption.",
#         "benefit": "Reduces stomach acid."
#     },
#     "Amoxicillin": {
#         "risk": "Allergic reactions, diarrhea.",
#         "benefit": "Treats bacterial infections."
#     },
#     "Hydrochlorothiazide": {
#         "risk": "Electrolyte imbalance, dehydration.",
#         "benefit": "Diuretic for high blood pressure."
#     },
#     "Clopidogrel": {
#         "risk": "Bleeding risk, rash.",
#         "benefit": "Prevents blood clots."
#     },
#     "Vitamin D": {
#         "risk": "High calcium levels if overdosed.",
#         "benefit": "Supports bone health."
#     },
#     "Calcium Carbonate": {
#         "risk": "Kidney stones, constipation.",
#         "benefit": "Prevents/treats calcium deficiency."
#     },
#     "Zinc Sulfate": {
#         "risk": "Nausea, metallic taste.",
#         "benefit": "Boosts immunity."
#     },
#     "Iron (Ferrous Sulfate)": {
#         "risk": "Constipation, dark stools.",
#         "benefit": "Treats iron deficiency anemia."
#     },
#     "Probiotic Capsules": {
#         "risk": "Bloating, gas (rare).",
#         "benefit": "Supports gut health."
#     },
#     "Aspirin": {
#         "risk": "Bleeding, stomach irritation.",
#         "benefit": "Pain relief, blood thinner."
#     }
# }

# # Load and save reminders
# def load_reminders():
#     if os.path.exists(REMINDER_FILE):
#         with open(REMINDER_FILE, "r") as f:
#             return json.load(f)
#     else:
#         today = datetime.now().strftime("%d/%m/%Y")
#         sample = {
#             today: [
#                 {
#                     "time": "16:58",
#                     "text": "Take Paracetamol",
#                     "medication": "Paracetamol",
#                     "risk": medication_info["Paracetamol"]["risk"],
#                     "benefit": medication_info["Paracetamol"]["benefit"]
#                 }
#             ]
#         }
#         save_reminders(sample)
#         return sample

# def save_reminders(reminders):
#     with open(REMINDER_FILE, "w") as f:
#         json.dump(reminders, f)

# reminders = load_reminders()

# # GUI setup
# root = tk.Tk()
# root.title("AI Calendar Reminder")
# root.geometry("850x700")
# root.configure(bg="#f0f0f0")

# style = ttk.Style(root)
# style.configure("TButton", font=("Segoe UI", 10), padding=6)
# style.configure("TLabel", font=("Segoe UI", 11))

# # Calendar widget
# cal_frame = tk.Frame(root)
# cal_frame.pack(pady=10)

# cal = Calendar(cal_frame, selectmode='day', date_pattern='dd/mm/yyyy')
# cal.pack()

# selected_date = cal.get_date()

# # Reminder display
# reminder_list_frame = tk.Frame(root, bg="#f0f0f0")
# reminder_list_frame.pack(pady=10)

# reminder_label = ttk.Label(reminder_list_frame, text=f"Reminders for {selected_date}:", font=("Segoe UI", 12, "bold"))
# reminder_label.pack()

# reminder_container = tk.Frame(reminder_list_frame, bg="#f0f0f0")
# reminder_container.pack()

# def refresh_reminders():
#     for widget in reminder_container.winfo_children():
#         widget.destroy()

#     reminder_label.config(text=f"Reminders for {selected_date}:")

#     if selected_date in reminders:
#         for idx, reminder in enumerate(reminders[selected_date]):
#             frame = tk.Frame(reminder_container, bg="#f0f0f0")
#             frame.pack(anchor='w', pady=2)

#             med = f" ({reminder['medication']})" if reminder.get("medication") else ""
#             risk = f" - Risk: {reminder['risk']}" if reminder.get("risk") else ""
#             benefit = f" - Benefit: {reminder['benefit']}" if reminder.get("benefit") else ""
#             reminder_text = ttk.Label(frame, text=f"{idx + 1}. {reminder['time']} - {reminder['text']}{med}{risk}{benefit}", font=("Segoe UI", 11))
#             reminder_text.pack(side=tk.LEFT, padx=5)

#             delete_btn = ttk.Button(frame, text="Delete", command=lambda i=idx: delete_reminder(i))
#             delete_btn.pack(side=tk.LEFT, padx=5)

# def delete_reminder(index):
#     reminders[selected_date].pop(index)
#     if not reminders[selected_date]:
#         reminders.pop(selected_date)
#     save_reminders(reminders)
#     refresh_calendar_tags()
#     refresh_reminders()

# # Add reminder section
# add_frame = tk.Frame(root, bg="#f0f0f0")
# add_frame.pack(pady=20)

# reminder_entry = ttk.Entry(add_frame, width=30)
# reminder_entry.insert(0, "Take your medication")
# reminder_entry.pack(side=tk.LEFT, padx=5)

# time_entry = ttk.Entry(add_frame, width=10)
# time_entry.insert(0, "HH:MM")
# time_entry.pack(side=tk.LEFT, padx=5)

# med_var = tk.StringVar()
# med_dropdown = ttk.Combobox(add_frame, textvariable=med_var, width=20)
# med_dropdown['values'] = list(medication_info.keys())
# med_dropdown.set("Paracetamol")
# med_dropdown.pack(side=tk.LEFT, padx=5)

# risk_var = tk.StringVar()
# risk_dropdown = ttk.Combobox(add_frame, textvariable=risk_var, width=40)
# risk_dropdown.set(medication_info["Paracetamol"]["risk"])
# risk_dropdown.pack(side=tk.LEFT, padx=5)

# benefit_var = tk.StringVar()
# benefit_dropdown = ttk.Combobox(add_frame, textvariable=benefit_var, width=40)
# benefit_dropdown.set(medication_info["Paracetamol"]["benefit"])
# benefit_dropdown.pack(side=tk.LEFT, padx=5)

# def update_info_dropdown(event):
#     selected_med = med_var.get()
#     risk = medication_info.get(selected_med, {}).get("risk", "")
#     benefit = medication_info.get(selected_med, {}).get("benefit", "")
#     risk_var.set(risk)
#     benefit_var.set(benefit)

# med_dropdown.bind("<<ComboboxSelected>>", update_info_dropdown)

# def add_reminder():
#     note = reminder_entry.get().strip()
#     time_str = time_entry.get().strip()
#     med = med_var.get().strip()
#     risk = risk_var.get().strip()
#     benefit = benefit_var.get().strip()
#     if not note or not time_str or not med or not risk or not benefit:
#         messagebox.showwarning("Empty", "Please fill all fields.")
#         return

#     new_entry = {"time": time_str, "text": note, "medication": med, "risk": risk, "benefit": benefit}
#     if selected_date in reminders:
#         reminders[selected_date].append(new_entry)
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

# Medication info
medication_info = {
    "Paracetamol": {"risk": "Liver damage if overdosed", "benefit": "Reduces fever and pain"},
    "Ibuprofen": {"risk": "Stomach ulcers, kidney issues", "benefit": "Anti-inflammatory, pain relief"},
    "Cetirizine": {"risk": "Drowsiness, dry mouth", "benefit": "Relieves allergies"},
    "Dextromethorphan": {"risk": "Dizziness, confusion", "benefit": "Suppresses cough"},
    "Losartan": {"risk": "Dizziness, high potassium", "benefit": "Lowers blood pressure"},
    "Amlodipine": {"risk": "Swelling, fatigue", "benefit": "Treats hypertension"},
    "Levocetirizine": {"risk": "Drowsiness", "benefit": "Relieves allergy symptoms"},
    "Chlorpheniramine": {"risk": "Sedation", "benefit": "Cold and allergy relief"},
    "Metformin": {"risk": "Lactic acidosis", "benefit": "Controls blood sugar"},
    "Atorvastatin": {"risk": "Muscle pain", "benefit": "Lowers cholesterol"},
    "Omeprazole": {"risk": "Nutrient malabsorption", "benefit": "Reduces stomach acid"},
    "Amoxicillin": {"risk": "Allergic reaction", "benefit": "Treats infections"},
    "Hydrochlorothiazide": {"risk": "Dehydration", "benefit": "Lowers blood pressure"},
    "Clopidogrel": {"risk": "Bleeding", "benefit": "Prevents blood clots"},
    "Vitamin D": {"risk": "High calcium levels", "benefit": "Supports bone health"},
    "Calcium Carbonate": {"risk": "Kidney stones", "benefit": "Strengthens bones"},
    "Zinc Sulfate": {"risk": "Nausea", "benefit": "Boosts immunity"},
    "Iron (Ferrous Sulfate)": {"risk": "Constipation", "benefit": "Treats anemia"},
    "Probiotic Capsules": {"risk": "Gas, bloating", "benefit": "Improves gut health"},
    "Aspirin": {"risk": "Bleeding", "benefit": "Pain relief, blood thinner"}
}

# Load reminders
def load_reminders():
    if os.path.exists(REMINDER_FILE):
        with open(REMINDER_FILE, "r") as f:
            return json.load(f)
    today = datetime.now().strftime("%d/%m/%Y")
    sample = {
        today: [{
            "time": "17:00",
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
    selected_med = med_var.get()
    risk = medication_info.get(selected_med, {}).get("risk", "")
    benefit = medication_info.get(selected_med, {}).get("benefit", "")
    risk_var.set(risk)
    benefit_var.set(benefit)

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
    risk_dropdown.set(medication_info["Paracetamol"]["risk"])
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
