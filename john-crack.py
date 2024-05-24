import subprocess
import tkinter as tk
from tkinter import filedialog

JOHN_PATH = r"C:\Users\aelhocine\Documents\Master CyberSécurité\Projet Cybersécurité (TOOLBOX)\Projet-Toolbox\john-1.9.0-jumbo-1-win64\john.exe"

def run_john(password_file, options):
    command = [JOHN_PATH, password_file] + options
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout

def select_file():
    filename = filedialog.askopenfilename(title="Select Password File")
    return filename

def select_options():
    options = []
    if checkbox1_var.get():
        options.append("--format=NT")
    if checkbox2_var.get():
        options.append("--format=SHA512")
    # Add more options as needed
    return options

def crack_password():
    password_file = select_file()
    if not password_file:
        return
    options = select_options()
    output = run_john(password_file, options)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, output)

# Create GUI
root = tk.Tk()
root.title("John the Ripper Password Cracker")

file_button = tk.Button(root, text="Select Password File", command=select_file)
file_button.pack()

checkbox1_var = tk.BooleanVar()
checkbox1 = tk.Checkbutton(root, text="NT Hash", variable=checkbox1_var)
checkbox1.pack()

checkbox2_var = tk.BooleanVar()
checkbox2 = tk.Checkbutton(root, text="SHA512 Hash", variable=checkbox2_var)
checkbox2.pack()

# Add more checkboxes for additional options

crack_button = tk.Button(root, text="Crack Password", command=crack_password)
crack_button.pack()

output_text = tk.Text(root, height=10, width=50)
output_text.pack()

root.mainloop()
