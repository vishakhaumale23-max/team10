import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
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

# Load and save reminders
def load_reminders():
    if os.path.exists(REMINDER_FILE):
        with open(REMINDER_FILE, "r") as f:
            data = json.load(f)
            # Convert old string format to dict
            for date in data:
                data[date] = [
                    {"time": "09:00", "text": r} if isinstance(r, str) else r
                    for r in data[date]
                ]
            return data
    else:
        today = datetime.now().strftime("%d/%m/%Y")
        sample = {
            today: [
                {"time": "16:37", "text": "Take blood pressure medication"},
                {"time": "16:38", "text": "Drink water"},
                {"time": "16:39", "text": "Stretch for 5 minutes"}
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
root.geometry("750x650")
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

            reminder_text = ttk.Label(frame, text=f"{idx + 1}. {reminder['time']} - {reminder['text']}", font=("Segoe UI", 11))
            reminder_text.pack(side=tk.LEFT, padx=5)

            edit_btn = ttk.Button(frame, text="Edit", command=lambda i=idx: edit_reminder(i))
            edit_btn.pack(side=tk.LEFT, padx=5)

            delete_btn = ttk.Button(frame, text="Delete", command=lambda i=idx: delete_reminder(i))
            delete_btn.pack(side=tk.LEFT, padx=5)

def edit_reminder(index):
    new_text = simpledialog.askstring("Edit Reminder", "Enter new reminder text:")
    new_time = simpledialog.askstring("Edit Time", "Enter new time (HH:MM):")
    if new_text and new_time:
        reminders[selected_date][index] = {"time": new_time, "text": new_text}
        save_reminders(reminders)
        refresh_calendar_tags()
        refresh_reminders()

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

reminder_entry = ttk.Entry(add_frame, width=40)
reminder_entry.pack(side=tk.LEFT, padx=5)

time_entry = ttk.Entry(add_frame, width=10)
time_entry.pack(side=tk.LEFT, padx=5)
time_entry.insert(0, "HH:MM")

def add_reminder():
    note = reminder_entry.get().strip()
    time_str = time_entry.get().strip()
    if not note or not time_str:
        messagebox.showwarning("Empty", "Please enter both reminder and time.")
        return

    if selected_date in reminders:
        reminders[selected_date].append({"time": time_str, "text": note})
    else:
        reminders[selected_date] = [{"time": time_str, "text": note}]
    save_reminders(reminders)
    refresh_calendar_tags()
    refresh_reminders()
    reminder_entry.delete(0, tk.END)
    time_entry.delete(0, tk.END)

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
                prompt = f"Send a friendly reminder to the user: '{reminder['text']}'"
                try:
                    response = ollama.chat(model='llama2', messages=[{"role": "user", "content": prompt}])
                    message = response['message']['content']
                except:
                    message = reminder['text']

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
