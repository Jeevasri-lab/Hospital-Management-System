
import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database connection and table creation
def create_database():
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            disease TEXT
        )
    """)

    conn.commit()
    conn.close()


# Add patient details
def save_patient():
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    gender = gender_entry.get().strip()
    disease = disease_entry.get().strip()

    if not name:
        messagebox.showerror("Error", "Please enter patient name.")
        return

    if age and not age.isdigit():
        messagebox.showerror("Error", "Age must be a number.")
        return

    if age and int(age) > 130:
        messagebox.showerror("Error", "Please enter a valid age.")
        return

    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO patients (name, age, gender, disease)
        VALUES (?, ?, ?, ?)
    """, (name, int(age) if age else None, gender, disease))

    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Patient added successfully!")

    clear_fields()
    # View all patients
def view_patients():
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients")
    records = cursor.fetchall()

    conn.close()

    view_window = tk.Toplevel(root)
    view_window.title("View Patients")
    view_window.geometry("700x350")
    view_window.configure(bg="white")

    tk.Label(
        view_window,
        text="Patient Records",
        font=("Arial", 18, "bold"),
        bg="white",
        fg="#123A70"
    ).pack(pady=10)

    text_box = tk.Text(
        view_window,
        width=80,
        height=15,
        font=("Courier New", 10),
        bg="white",
        fg="black"
    )
    text_box.pack(padx=10, pady=10)

    text_box.insert(
        tk.END,
        "ID | Name | Age | Gender | Disease\n"
    )
    text_box.insert(tk.END, "-" * 65 + "\n")

    if records:
        for patient in records:
            text_box.insert(
                tk.END,
                f"{patient[0]} | {patient[1]} | "
                f"{patient[2]} | {patient[3]} | {patient[4]}\n"
            )
    else:
        text_box.insert(tk.END, "No patient records found.\n")

    text_box.config(state="disabled")
# Search patient by ID
def search_patient():
    search_window = tk.Toplevel(root)
    search_window.title("Search Patient")
    search_window.geometry("450x250")
    search_window.configure(bg="white")

    tk.Label(
        search_window,
        text="Enter Patient ID:",
        font=("Arial", 13),
        bg="white",
        fg="black"
    ).pack(pady=15)

    id_entry = tk.Entry(
        search_window,
        font=("Arial", 13),
        bg="white",
        fg="black"
    )
    id_entry.pack(pady=5)

    def find_patient():
        patient_id = id_entry.get().strip()

        if not patient_id.isdigit():
            messagebox.showerror(
                "Error", "Enter a valid Patient ID."
            )
            return

        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM patients WHERE patient_id = ?",
            (int(patient_id),)
        )
        patient = cursor.fetchone()
        conn.close()

        if patient:
            messagebox.showinfo(
                "Patient Found",
                f"ID: {patient[0]}\n"
                f"Name: {patient[1]}\n"
                f"Age: {patient[2]}\n"
                f"Gender: {patient[3]}\n"
                f"Disease: {patient[4]}"
            )
        else:
            messagebox.showwarning(
                "Not Found", "Patient ID not found."
            )

    tk.Button(
        search_window,
        text="Search",
        font=("Arial", 12),
        command=find_patient
    ).pack(pady=15)
# Update patient details
def update_patient():
    update_window = tk.Toplevel(root)
    update_window.title("Update Patient")
    update_window.geometry("450x400")
    update_window.configure(bg="white")

    tk.Label(
        update_window,
        text="Patient ID:",
        font=("Arial", 12),
        bg="white",
        fg="black"
    ).pack(pady=5)

    id_entry = tk.Entry(
        update_window, font=("Arial", 12),
        bg="white", fg="black"
    )
    id_entry.pack(pady=5)

    tk.Label(
        update_window,
        text="New Name:",
        font=("Arial", 12),
        bg="white",
        fg="black"
    ).pack(pady=5)

    name_input = tk.Entry(
        update_window, font=("Arial", 12),
        bg="white", fg="black"
    )
    name_input.pack(pady=5)

    tk.Label(
        update_window,
        text="New Age:",
        font=("Arial", 12),
        bg="white",
        fg="black"
    ).pack(pady=5)

    age_input = tk.Entry(
        update_window, font=("Arial", 12),
        bg="white", fg="black"
    )
    age_input.pack(pady=5)

    tk.Label(
        update_window,
        text="New Gender:",
        font=("Arial", 12),
        bg="white",
        fg="black"
    ).pack(pady=5)

    gender_input = tk.Entry(
        update_window, font=("Arial", 12),
        bg="white", fg="black"
    )
    gender_input.pack(pady=5)

    tk.Label(
        update_window,
        text="New Disease:",
        font=("Arial", 12),
        bg="white",
        fg="black"
    ).pack(pady=5)

    disease_input = tk.Entry(
        update_window, font=("Arial", 12),
        bg="white", fg="black"
    )
    disease_input.pack(pady=5)

    def save_update():
        patient_id = id_entry.get().strip()
        name = name_input.get().strip()
        age = age_input.get().strip()
        gender = gender_input.get().strip()
        disease = disease_input.get().strip()

        if not patient_id.isdigit():
            messagebox.showerror(
                "Error", "Enter a valid Patient ID."
            )
            return

        if not name:
            messagebox.showerror(
                "Error", "Patient name is required."
            )
            return

        if age and not age.isdigit():
            messagebox.showerror(
                "Error", "Age must be a number."
            )
            return

        if age and int(age) > 130:
            messagebox.showerror(
                "Error", "Please enter a valid age."
            )
            return

        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE patients
            SET name = ?, age = ?, gender = ?, disease = ?
            WHERE patient_id = ?
        """, (
            name,
            int(age) if age else None,
            gender,
            disease,
            int(patient_id)
        ))

        updated = cursor.rowcount
        conn.commit()
        conn.close()

        if updated:
            messagebox.showinfo(
                "Success", "Patient details updated!"
            )
            update_window.destroy()
        else:
            messagebox.showwarning(
                "Not Found", "Patient ID not found."
            )

    tk.Button(
        update_window,
        text="Update Patient",
        font=("Arial", 12),
        command=save_update
    ).pack(pady=15)
# Delete patient by ID
def delete_patient():
    delete_window = tk.Toplevel(root)
    delete_window.title("Delete Patient")
    delete_window.geometry("400x220")
    delete_window.configure(bg="white")

    tk.Label(
        delete_window,
        text="Enter Patient ID to Delete:",
        font=("Arial", 13),
        bg="white",
        fg="black"
    ).pack(pady=20)

    id_entry = tk.Entry(
        delete_window,
        font=("Arial", 13),
        bg="white",
        fg="black"
    )
    id_entry.pack(pady=5)

    def confirm_delete():
        patient_id = id_entry.get().strip()

        if not patient_id.isdigit():
            messagebox.showerror(
                "Error", "Enter a valid Patient ID."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete Patient ID {patient_id}?"
        )

        if not confirm:
            return

        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM patients WHERE patient_id = ?",
            (int(patient_id),)
        )

        deleted = cursor.rowcount
        conn.commit()
        conn.close()

        if deleted:
            messagebox.showinfo(
                "Success", "Patient deleted successfully!"
            )
            delete_window.destroy()
        else:
            messagebox.showwarning(
                "Not Found", "Patient ID not found."
            )

    tk.Button(
        delete_window,
        text="Delete Patient",
        font=("Arial", 12),
        command=confirm_delete
    ).pack(pady=15)        
# Clear all input fields
def clear_fields():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    gender_entry.delete(0, tk.END)
    disease_entry.delete(0, tk.END)


# Main application window
create_database()

root = tk.Tk()
root.title("Hospital Management System")
root.geometry("750x600")
root.configure(bg="#F2F6FC")
root.resizable(False, False)

# Heading
heading = tk.Label(
    root,
    text="Hospital Management System",
    font=("Arial", 22, "bold"),
    bg="#F2F6FC",
    fg="#123A70"
)
heading.pack(pady=30)

# Form container
form = tk.Frame(root, bg="white", padx=35, pady=25)
form.pack(pady=10)

# Common label style
label_style = {
    "font": ("Arial", 13),
    "bg": "white",
    "fg": "#222222",
    "anchor": "w"
}

# Common entry style
entry_style = {
    "font": ("Arial", 13),
    "bg": "white",
    "fg": "black",
    "insertbackground": "black",
    "width": 30,
    "relief": "solid",
    "bd": 1
}

# Patient Name
tk.Label(
    form, text="Patient Name:", **label_style
).grid(row=0, column=0, padx=12, pady=12, sticky="w")

name_entry = tk.Entry(form, **entry_style)
name_entry.grid(row=0, column=1, padx=12, pady=12)

# Age
tk.Label(
    form, text="Age:", **label_style
).grid(row=1, column=0, padx=12, pady=12, sticky="w")

age_entry = tk.Entry(form, **entry_style)
age_entry.grid(row=1, column=1, padx=12, pady=12)

# Gender
tk.Label(
    form, text="Gender:", **label_style
).grid(row=2, column=0, padx=12, pady=12, sticky="w")

gender_entry = tk.Entry(form, **entry_style)
gender_entry.grid(row=2, column=1, padx=12, pady=12)

# Disease
tk.Label(
    form, text="Disease:", **label_style
).grid(row=3, column=0, padx=12, pady=12, sticky="w")

disease_entry = tk.Entry(form, **entry_style)
disease_entry.grid(row=3, column=1, padx=12, pady=12)

# Buttons
button_frame = tk.Frame(root, bg="#F2F6FC")
button_frame.pack(pady=25)

add_button = tk.Button(
    button_frame,
    text="Add Patient",
    font=("Arial", 13, "bold"),
    bg="#1769AA",
    fg="white",
    activebackground="#0F4C81",
    activeforeground="white",
    width=15,
    command=save_patient
)
add_button.grid(row=0, column=0, padx=10)
view_button = tk.Button(
    button_frame,
    text="View Patients",
    font=("Arial", 13, "bold"),
    bg="#1769AA",
    fg="white",
    activebackground="#0F4C81",
    activeforeground="white",
    width=15,
    command=view_patients
)
view_button.grid(row=1, column=0, padx=10, pady=10)
search_button = tk.Button(
    button_frame,
    text="Search Patient",
    font=("Arial", 13, "bold"),
    bg="#1769AA",
    fg="white",
    activebackground="#0F4C81",
    activeforeground="white",
    width=15,
    command=search_patient
)
search_button.grid(row=1, column=1, padx=10, pady=10)
update_button = tk.Button(
    button_frame,
    text="Update Patient",
    font=("Arial", 13, "bold"),
    bg="#1769AA",
    fg="white",
    activebackground="#0F4C81",
    activeforeground="white",
    width=15,
    command=update_patient
)
update_button.grid(row=2, column=0, padx=10, pady=10)
delete_button = tk.Button(
    button_frame,
    text="Delete Patient",
    font=("Arial", 13, "bold"),
    bg="#B83232",
    fg="white",
    activebackground="#8B2020",
    activeforeground="white",
    width=15,
    command=delete_patient
)
delete_button.grid(row=2, column=1, padx=10, pady=10)
clear_button = tk.Button(
    button_frame,
    text="Clear Fields",
    font=("Arial", 13),
    bg="#DDE5EF",
    fg="#222222",
    width=15,
    command=clear_fields
)
clear_button.grid(row=0, column=1, padx=10)

exit_button = tk.Button(
    button_frame,
    text="Exit",
    font=("Arial", 13),
    bg="#B83232",
    fg="white",
    width=10,
    command=root.destroy
)
exit_button.grid(row=0, column=2, padx=10)

# Start application
root.mainloop()
