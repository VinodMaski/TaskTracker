import tkinter
import tkinter.messagebox
import pickle
import datetime

root = tkinter.Tk()
root.title("To-Do List ")

def add_task():
    task = entry_task.get()
    hours = entry_hours.get()
    minutes = entry_minutes.get()
    notification_minutes = entry_notification.get()  # Retrieve notification time in minutes

    if task != "":
        if hours.isdigit() and minutes.isdigit() and notification_minutes.isdigit() and int(hours) < 24 and int(minutes) < 60:
            current_time = datetime.datetime.now()
            scheduled_time = datetime.datetime(current_time.year, current_time.month, current_time.day, int(hours), int(minutes))

            notification_time = scheduled_time - datetime.timedelta(minutes=int(notification_minutes))

            if current_time < notification_time:
                time_diff = notification_time - current_time
                seconds_diff = time_diff.total_seconds()
                root.after(int(seconds_diff * 1000), show_notification, task)

            # Combine task, hours, and minutes into a single string
            task_with_time = f"{hours}:{minutes} - {task}"
            listbox_tasks.insert(tkinter.END, task_with_time)

            entry_task.delete(0, tkinter.END)
            entry_hours.delete(0, tkinter.END)
            entry_minutes.delete(0, tkinter.END)
            entry_notification.delete(0, tkinter.END)
        else:
            tkinter.messagebox.showwarning(title="Warning!", message="Invalid time or notification minutes.")
    else:
        tkinter.messagebox.showwarning(title="Warning!", message="You must enter a task.")

def show_notification(task):
    tkinter.messagebox.showinfo(title="Task Notification", message=f"It's time to do the task: {task}")

def delete_task():
    try:
        task_index = listbox_tasks.curselection()[0]
        listbox_tasks.delete(task_index)
    except:
        tkinter.messagebox.showwarning(title="Warning!", message="You must select a task.")

def load_tasks():
    try:
        tasks = pickle.load(open("tasks.dat", "rb"))
        listbox_tasks.delete(0, tkinter.END)
        for task in tasks:
            listbox_tasks.insert(tkinter.END, task)
    except:
        tkinter.messagebox.showwarning(title="Warning!", message="Cannot find tasks.dat.")

def save_tasks():
    tasks = listbox_tasks.get(0, listbox_tasks.size())
    pickle.dump(tasks, open("tasks.dat", "wb"))

# Create GUI
frame_tasks = tkinter.Frame(root)
frame_tasks.pack()

listbox_tasks = tkinter.Listbox(frame_tasks, height=10, width=50)
listbox_tasks.pack(side=tkinter.LEFT)

scrollbar_tasks = tkinter.Scrollbar(frame_tasks)
scrollbar_tasks.pack(side=tkinter.RIGHT, fill=tkinter.Y)

listbox_tasks.config(yscrollcommand=scrollbar_tasks.set)
scrollbar_tasks.config(command=listbox_tasks.yview)

entry_task = tkinter.Entry(root, width=45)
entry_task.pack()

entry_hours = tkinter.Entry(root, width=10)
entry_hours.pack()

entry_minutes = tkinter.Entry(root, width=10)
entry_minutes.pack()

entry_notification = tkinter.Entry(root, width=10)  # Entry field for notification time in minutes
entry_notification.pack()

button_add_task = tkinter.Button(root, text="Add task", width=48, command=add_task)
button_add_task.pack()

button_delete_task = tkinter.Button(root, text="Delete task", width=48, command=delete_task)
button_delete_task.pack()

button_load_tasks = tkinter.Button(root, text="Load tasks", width=48, command=load_tasks)
button_load_tasks.pack()

button_save_tasks = tkinter.Button(root, text="Save tasks", width=48, command=save_tasks)
button_save_tasks.pack()

root.mainloop()