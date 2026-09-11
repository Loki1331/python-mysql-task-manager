import mysql.connector
from tabulate import tabulate
from datetime import date

# ------------------- DATABASE CONNECTION -------------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="....",#enter the password which you enter in the sql
    database="task_manager"
)

cur = db.cursor()

# ------------------- ADD TASK -------------------
def add_task():
    desc = input("Enter task description: ")
    due = input("Enter due date (YYYY-MM-DD): ")
    priority = input("Enter priority (LOW / MEDIUM / HIGH): ")

    today = str(date.today())

    cur.execute(
        "INSERT INTO tasks (task_description, due_date, status, date_created, priority) VALUES (%s, %s, %s, %s, %s)",
        (desc, due, "Pending", today, priority)
    )
    db.commit()
    print("\nTask added successfully!\n")

# ------------------- VIEW ALL TASKS -------------------
def view_all_tasks():
    cur.execute("SELECT task_id, task_description, due_date, status, priority FROM tasks")
    rows = cur.fetchall()
    print(tabulate(rows, headers=["ID", "Task", "Due Date", "Status", "Priority"], tablefmt="grid"))

# ------------------- VIEW PENDING TASKS -------------------
def view_pending_tasks():
    cur.execute("SELECT task_id, task_description, due_date, status, priority FROM tasks WHERE status='Pending'")
    rows = cur.fetchall()
    print(tabulate(rows, headers=["ID", "Task", "Due Date", "Status", "Priority"], tablefmt="grid"))

# ------------------- VIEW COMPLETED TASKS -------------------
def view_completed_tasks():
    cur.execute("SELECT task_id, task_description, due_date, status, priority FROM tasks WHERE status='Completed'")
    rows = cur.fetchall()
    print(tabulate(rows, headers=["ID", "Task", "Due Date", "Status", "Priority"], tablefmt="grid"))

# ------------------- UPDATE TASK DETAILS -------------------
def update_task_details():
    tid = input("Enter Task ID to update: ")
    print("Leave any field blank to skip updating.")

    newdesc = input("New task description: ")
    newdue = input("New due date (YYYY-MM-DD): ")
    newpriority = input("New priority (LOW / MEDIUM / HIGH): ")

    if newdesc.strip():
        cur.execute("UPDATE tasks SET task_description=%s WHERE task_id=%s", (newdesc, tid))

    if newdue.strip():
        cur.execute("UPDATE tasks SET due_date=%s WHERE task_id=%s", (newdue, tid))

    if newpriority.strip():
        cur.execute("UPDATE tasks SET priority=%s WHERE task_id=%s", (newpriority, tid))

    db.commit()
    print("\nTask details updated!\n")

# ------------------- UPDATE STATUS -------------------
def update_status():
    tid = input("Enter Task ID: ")
    newstatus = input("Enter status (Pending / In-Progress / Completed): ")

    cur.execute("UPDATE tasks SET status=%s WHERE task_id=%s", (newstatus, tid))
    db.commit()
    print("\nTask status updated!\n")

# ------------------- DELETE TASK -------------------
def delete_task():
    tid = input("Enter Task ID to delete: ")
    cur.execute("DELETE FROM tasks WHERE task_id=%s", (tid,))
    db.commit()
    print("\nTask deleted successfully!\n")

# ------------------- VIEW HIGH PRIORITY TASKS -------------------
def view_high_priority():
    cur.execute("SELECT task_id, task_description, due_date, status, priority FROM tasks WHERE priority='HIGH'")
    rows = cur.fetchall()
    print(tabulate(rows, headers=["ID", "Task", "Due Date", "Status", "Priority"], tablefmt="grid"))

# ------------------- VIEW LOW PRIORITY TASKS -------------------
def view_low_priority():
    cur.execute("SELECT task_id, task_description, due_date, status, priority FROM tasks WHERE priority='LOW'")
    rows = cur.fetchall()
    print(tabulate(rows, headers=["ID", "Task", "Due Date", "Status", "Priority"], tablefmt="grid"))

# ------------------- SEARCH TASK -------------------
def search_task():
    key = input("Enter keyword to search: ")
    cur.execute(
        "SELECT task_id, task_description, due_date, status, priority FROM tasks WHERE task_description LIKE %s",
        (f"%{key}%",)
    )
    rows = cur.fetchall()
    print(tabulate(rows, headers=["ID", "Task", "Due Date", "Status", "Priority"], tablefmt="grid"))

# ------------------- MAIN MENU -------------------
def main_menu():
    while True:
        print("\n===== TO-DO LIST MANAGER =====")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. View Pending Tasks")
        print("4. View Completed Tasks")
        print("5. Update Task Description / Due Date / Priority")
        print("6. Update Task Status")
        print("7. Delete Task")
        print("8. View HIGH Priority Tasks")
        print("9. View LOW Priority Tasks")
        print("10. Search Task")
        print("11. Exit")

        ch = input("Enter choice: ")

        if ch == "1":
            add_task()
        elif ch == "2":
            view_all_tasks()
        elif ch == "3":
            view_pending_tasks()
        elif ch == "4":
            view_completed_tasks()
        elif ch == "5":
            update_task_details()
        elif ch == "6":
            update_status()
        elif ch == "7":
            delete_task()
        elif ch == "8":
            view_high_priority()
        elif ch == "9":
            view_low_priority()
        elif ch == "10":
            search_task()
        elif ch == "11":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice!")

main_menu()