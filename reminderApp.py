import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import Calendar
from datetime import datetime
from plyer import notification
import winsound
import json
import os

#Data Setup
REMINDER_FILE = "reminders.json"

def load_reminders():
    if os.path.exists(REMINDER_FILE):
        with open(REMINDER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_reminders(reminders):
    with open(REMINDER_FILE, "w") as f:
        json.dump(reminders, f)

reminders = load_reminders()

#GUI Setup
root = tk.Tk()
root.title("Calendar & Reminder App")
root.geometry("750x650")
import os
icon_path = r"C:\code\healthcare\icon.ico"
root.iconbitmap(icon_path)
root.configure(bg="#f0f0f0")

style = ttk.Style(root)
style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.configure("TLabel", font=("Segoe UI", 11))

#Calendar
cal_frame = tk.Frame(root)
cal_frame.pack(pady=10)

cal = Calendar(
    cal_frame,
    selectmode='day',
    date_pattern='dd/mm/yyyy',
    showweeknumbers=False,
    font=("Segoe UI", 12),
    background="white",
    foreground="black",
    headersbackground="#dbe6fd",
    headersforeground="black",
    normalbackground="#f0f8ff",
    normalforeground="black",
    weekendbackground="#f0f8ff",
    weekendforeground="black",
    othermonthbackground="#f9f9f9",
    othermonthwebackground="#f9f9f9",
    othermonthforeground="#aaa",
    bordercolor="#4a7abc",
    selectbackground="#4a7abc",
    selectforeground="white",
    locale="en_US"
)
cal.pack()

#Reminder Display
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

            reminder_text = ttk.Label(frame, text=f"{idx + 1}. {reminder}", font=("Segoe UI", 11))
            reminder_text.pack(side=tk.LEFT, padx=5)

            edit_btn = ttk.Button(frame, text="Edit", command=lambda i=idx: edit_reminder(i))
            edit_btn.pack(side=tk.LEFT, padx=5)

            delete_btn = ttk.Button(frame, text="Delete", command=lambda i=idx: delete_reminder(i))
            delete_btn.pack(side=tk.LEFT, padx=5)

def edit_reminder(index):
    new_text = simpledialog.askstring("Edit Reminder", "Enter new reminder text:")
    if new_text:
        reminders[selected_date][index] = new_text
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

#Add Reminder Section
add_frame = tk.Frame(root, bg="#f0f0f0")
add_frame.pack(pady=20)

reminder_entry = ttk.Entry(add_frame, width=50)
reminder_entry.pack(side=tk.LEFT, padx=5)

def add_reminder():
    note = reminder_entry.get().strip()
    if not note:
        messagebox.showwarning("Empty", "Please enter a reminder.")
        return

    if selected_date in reminders:
        reminders[selected_date].append(note)
    else:
        reminders[selected_date] = [note]
    save_reminders(reminders)
    refresh_calendar_tags()
    refresh_reminders()
    reminder_entry.delete(0, tk.END)

add_btn = ttk.Button(add_frame, text="Add Reminder", command=add_reminder)
add_btn.pack(side=tk.LEFT, padx=5)

#Calendar Click Handler
def on_date_click(event):
    global selected_date
    selected_date = cal.get_date()
    refresh_reminders()
    add_frame.pack_forget()
    add_frame.pack(pady=20)

cal.bind("<<CalendarSelected>>", on_date_click)

#Calendar Tagging
def refresh_calendar_tags():
    cal.calevent_remove('all')
    for date_str in reminders:
        try:
            dt = datetime.strptime(date_str, "%d/%m/%Y")
            cal.calevent_create(dt, "📌", "reminder")
        except:
            pass
    cal.tag_config("reminder", background="#fdf2dc", foreground="black")

#Init
refresh_calendar_tags()
refresh_reminders()

# Popup + system notification + system beep
today = datetime.now().strftime("%d/%m/%Y")
if today in reminders and reminders[today]:
    reminder_text = "\n".join(f"• {r}" for r in reminders[today])

    notification.notify(
        title="🔔 Today's Reminders",
        message=reminder_text,
        timeout=3
    )

    winsound.MessageBeep(winsound.MB_ICONASTERISK)

root.mainloop()