import csv
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

DATA_FILE = "assignment_tracker.json"


class AssignmentTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Assignment Tracker")
        self.root.geometry("900x600")
        self.records = []

        self.load_data()
        self.create_widgets()
        self.show_data()

    def load_data(self):
        try:
            with open(DATA_FILE, "r") as file:
                self.records = json.load(file)
        except:
            self.records = []

    def save_data(self):
        with open(DATA_FILE, "w") as file:
            json.dump(self.records, file, indent=4)

    def create_widgets(self):
        frame = ttk.Frame(self.root)
        frame.pack(pady=10)

        ttk.Label(frame, text="Enrollment").grid(row=0, column=0)
        ttk.Label(frame, text="Name").grid(row=0, column=2)
        ttk.Label(frame, text="Assignment").grid(row=1, column=0)
        ttk.Label(frame, text="Status").grid(row=1, column=2)
        ttk.Label(frame, text="Marks").grid(row=2, column=0)
        ttk.Label(frame, text="Remarks").grid(row=2, column=2)

        self.enrollment = ttk.Entry(frame)
        self.name = ttk.Entry(frame)
        self.assignment = ttk.Entry(frame)
        self.status = ttk.Combobox(
            frame,
            values=["Pending", "Completed"],
            state="readonly"
        )
        self.marks = ttk.Entry(frame)
        self.remarks = ttk.Entry(frame)

        self.enrollment.grid(row=0, column=1, padx=5, pady=5)
        self.name.grid(row=0, column=3, padx=5, pady=5)
        self.assignment.grid(row=1, column=1, padx=5, pady=5)
        self.status.grid(row=1, column=3, padx=5, pady=5)
        self.marks.grid(row=2, column=1, padx=5, pady=5)
        self.remarks.grid(row=2, column=3, padx=5, pady=5)

        self.status.set("Pending")

        ttk.Button(
            frame,
            text="Add / Update",
            command=self.add_record
        ).grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(
            frame,
            text="Export CSV",
            command=self.export_csv
        ).grid(row=3, column=2, columnspan=2, pady=10)

        ttk.Label(self.root, text="Filter").pack()

        self.filter_box = ttk.Combobox(
            self.root,
            values=["All", "Pending", "Completed"],
            state="readonly"
        )
        self.filter_box.set("All")
        self.filter_box.pack()
        self.filter_box.bind(
            "<<ComboboxSelected>>",
            lambda event: self.show_data()
        )

        columns = (
            "enrollment",
            "name",
            "assignment",
            "status",
            "marks",
            "remarks"
        )

        self.table = ttk.Treeview(
            self.root,
            columns=columns,
            show="headings"
        )
        self.table.pack(fill="both", expand=True, padx=10, pady=10)

        for column in columns:
            self.table.heading(column, text=column.title())
            self.table.column(column, width=130)

    def add_record(self):
        try:
            enrollment = self.enrollment.get().strip()
            name = self.name.get().strip()
            assignment = self.assignment.get().strip()
            status = self.status.get()
            marks = self.marks.get().strip()
            remarks = self.remarks.get().strip()

            if enrollment == "" or name == "" or assignment == "":
                raise Exception("Required fields are empty")

            if marks == "":
                marks_value = ""
            else:
                marks_value = float(marks)
                if marks_value < 0 or marks_value > 100:
                    raise Exception("Marks must be between 0 and 100")

            record = {
                "enrollment": enrollment,
                "name": name,
                "assignment": assignment,
                "status": status,
                "marks": marks_value,
                "remarks": remarks
            }

            found = False

            for old_record in self.records:
                if (
                    old_record["enrollment"] == enrollment
                    and old_record["assignment"] == assignment
                ):
                    old_record.update(record)
                    found = True
                    break

            if not found:
                self.records.append(record)

            self.save_data()
            self.show_data()
            messagebox.showinfo("Success", "Record saved")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_data(self):
        for item in self.table.get_children():
            self.table.delete(item)

        selected = self.filter_box.get()

        for record in self.records:
            if selected != "All" and record["status"] != selected:
                continue

            self.table.insert(
                "",
                "end",
                values=(
                    record["enrollment"],
                    record["name"],
                    record["assignment"],
                    record["status"],
                    record["marks"],
                    record["remarks"]
                )
            )

    def export_csv(self):
        if len(self.records) == 0:
            messagebox.showwarning("Export", "No records available")
            return

        file_name = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")]
        )

        if file_name == "":
            return

        fields = [
            "enrollment",
            "name",
            "assignment",
            "status",
            "marks",
            "remarks"
        ]

        with open(file_name, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(self.records)

        messagebox.showinfo("Export", "CSV file created")


root = tk.Tk()
app = AssignmentTracker(root)
root.mainloop()
