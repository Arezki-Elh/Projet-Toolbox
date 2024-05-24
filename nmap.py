# Importation des modules Tkinter pour l'interface graphique,
# ttk pour les widgets améliorés et scrolledtext pour la zone de texte déroulante.
import tkinter as tk  # Module principal pour l'interface graphique
from tkinter import ttk  # Contient des versions améliorées des widgets Tkinter
from tkinter import scrolledtext  # Fournit une zone de texte déroulante

# Importation des modules nécessaires pour le scan de ports.
import socket  # Fournit des fonctions pour la communication réseau
import threading  # Permet d'exécuter le scan dans un thread séparé
from datetime import datetime  # Permet d'obtenir la date et l'heure actuelles
import subprocess  # Utilisé pour exécuter la commande Nmap

# Classe principale de l'application, héritant de tk.Tk pour créer la fenêtre principale.
class PortScannerApp(tk.Tk):
    def __init__(self):
        super().__init__()  # Appel au constructeur de la classe parente
        self.title("Port Scanner")  # Définit le titre de la fenêtre
        self.geometry("500x400")    # Définit la taille de la fenêtre

        # Création des widgets pour l'interface utilisateur
        self.create_widgets()

        # Initialisation d'une variable pour stocker le thread de scan
        self.scan_thread = None

    # Méthode pour créer les widgets de l'interface utilisateur
    def create_widgets(self):
        # Étiquette et entrée pour l'adresse IP cible
        self.label_ip = ttk.Label(self, text="Adresse IP de la cible :")
        self.label_ip.grid(column=0, row=0, padx=10, pady=10)
        self.entry_ip = ttk.Entry(self)
        self.entry_ip.grid(column=1, row=0, padx=10, pady=10)

        # Étiquette et entrées pour la plage de ports à scanner
        self.label_ports = ttk.Label(self, text="Plage de ports à scanner (de - à) :")
        self.label_ports.grid(column=0, row=1, padx=10, pady=10)
        self.entry_start_port = ttk.Entry(self, width=5)
        self.entry_start_port.grid(column=1, row=1, padx=5, pady=10)
        self.entry_end_port = ttk.Entry(self, width=5)
        self.entry_end_port.grid(column=2, row=1, padx=5, pady=10)

        # Cases à cocher pour les options Nmap
        self.var_syn = tk.BooleanVar()
        self.check_syn = ttk.Checkbutton(self, text="Scan SYN (-sS)", variable=self.var_syn)
        self.check_syn.grid(column=0, row=3, padx=10, pady=5)

        self.var_version = tk.BooleanVar()
        self.check_version = ttk.Checkbutton(self, text="Détection de version (-sV)", variable=self.var_version)
        self.check_version.grid(column=1, row=3, padx=10, pady=5)

        self.var_os = tk.BooleanVar()
        self.check_os = ttk.Checkbutton(self, text="Détection du système d'exploitation (-O)", variable=self.var_os)
        self.check_os.grid(column=2, row=3, padx=10, pady=5)

        self.var_aggressive = tk.BooleanVar()
        self.check_aggressive = ttk.Checkbutton(self, text="Scan agressif (-A)", variable=self.var_aggressive)
        self.check_aggressive.grid(column=0, row=4, padx=10, pady=5)

        # Bouton pour démarrer le scan
        self.btn_scan = ttk.Button(self, text="Démarrer le scan", command=self.start_scan)
        self.btn_scan.grid(column=1, row=5, pady=10)

        # Zone de texte déroulante pour afficher les résultats du scan
        self.result_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=60, height=15)
        self.result_text.grid(column=0, row=6, columnspan=3, padx=10, pady=10)

    # Méthode appelée lors du clic sur le bouton "Démarrer le scan"
    def start_scan(self):
        # Validation des entrées utilisateur
        target_ip = self.entry_ip.get()
        start_port = self.entry_start_port.get()
        end_port = self.entry_end_port.get()

        if not target_ip or not start_port or not end_port:
            self.result_text.insert(tk.END, "Veuillez saisir une adresse IP cible et une plage de ports.\n")
            return

        try:
            start_port = int(start_port)
            end_port = int(end_port)
        except ValueError:
            self.result_text.insert(tk.END, "Veuillez saisir des numéros de port valides.\n")
            return

        if start_port > end_port:
            self.result_text.insert(tk.END, "Le port de début doit être inférieur ou égal au port de fin.\n")
            return

        # Construction de la commande Nmap en fonction des options sélectionnées
        nmap_cmd = "nmap"
        if self.var_syn.get():
            nmap_cmd += " -sS"
        if self.var_version.get():
            nmap_cmd += " -sV"
        if self.var_os.get():
            nmap_cmd += " -O"
        if self.var_aggressive.get():
            nmap_cmd += " -A"
        nmap_cmd += f" -p {start_port}-{end_port} {target_ip}"

        # Affichage d'un message indiquant le début du scan
        self.result_text.insert(tk.END, f"Balayage de ports sur {target_ip}...\n")

        # Lancement d'un thread pour exécuter la commande Nmap
        self.scan_thread = threading.Thread(target=self.run_nmap, args=(nmap_cmd,))
        self.scan_thread.start()

    # Méthode pour exécuter la commande Nmap dans un thread séparé
    def run_nmap(self, nmap_cmd):
        try:
            # Exécution de la commande Nmap et affichage des résultats dans la zone de texte déroulante
            output = subprocess.check_output(nmap_cmd, shell=True, universal_newlines=True)
            self.result_text.insert(tk.END, output)
        except subprocess.CalledProcessError as e:
            # Affichage d'un message en cas d'erreur lors de l'exécution de la commande Nmap
            self.result_text.insert(tk.END, f"Erreur lors de l'exécution de la commande Nmap : {e.output}\n")
        except Exception as e:
            # Affichage d'un message en cas d'erreur inattendue
            self.result_text.insert(tk.END, f"Erreur inattendue : {e}\n")

# Point d'entrée de l'application, exécute l'application si ce fichier est exécuté en tant que script
if __name__ == "__main__":
    app = PortScannerApp()  # Crée une instance de l'application
    app.mainloop()  # Démarre la boucle principale de l'interface graphique