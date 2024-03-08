import tkinter as tk  # Importe le module tkinter pour créer une interface graphique
from tkinter import ttk  # Importe le module ttk pour les widgets améliorés
from tkinter import scrolledtext  # Importe le module scrolledtext pour le widget de texte déroulant
import socket  # Importe le module socket pour les opérations de réseau
import threading  # Importe le module threading pour exécuter des tâches en parallèle
from datetime import datetime  # Importe la classe datetime pour la gestion du temps

class PortScannerApp(tk.Tk):
    def __init__(self):
        super().__init__()  # Initialise la classe parente Tkinter
        self.title("Port Scanner")  # Définit le titre de la fenêtre
        self.geometry("500x400")  # Définit la taille de la fenêtre

        # Crée une étiquette et une entrée pour l'adresse IP cible
        self.label_ip = ttk.Label(self, text="Adresse IP de la cible :")
        self.label_ip.grid(column=0, row=0, padx=10, pady=10)
        self.entry_ip = ttk.Entry(self)
        self.entry_ip.grid(column=1, row=0, padx=10, pady=10)

        # Crée une étiquette et deux entrées pour la plage de ports à scanner
        self.label_ports = ttk.Label(self, text="Plage de ports à scanner (de - à) :")
        self.label_ports.grid(column=0, row=1, padx=10, pady=10)
        self.entry_start_port = ttk.Entry(self, width=5)
        self.entry_start_port.grid(column=1, row=1, padx=5, pady=10)
        self.entry_end_port = ttk.Entry(self, width=5)
        self.entry_end_port.grid(column=2, row=1, padx=5, pady=10)

        # Crée un bouton pour démarrer le scan
        self.btn_scan = ttk.Button(self, text="Démarrer le scan", command=self.start_scan)
        self.btn_scan.grid(column=1, row=2, pady=10)

        # Crée une zone de texte déroulante pour afficher les résultats du scan
        self.result_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=60, height=15)
        self.result_text.grid(column=0, row=3, columnspan=3, padx=10, pady=10)

    def start_scan(self):
        target_ip = self.entry_ip.get()  # Récupère l'adresse IP saisie par l'utilisateur
        start_port = int(self.entry_start_port.get())  # Récupère le port de départ
        end_port = int(self.entry_end_port.get())  # Récupère le port de fin

        if not target_ip:  # Vérifie si l'adresse IP est vide
            self.result_text.insert(tk.END, "Veuillez saisir une adresse IP cible.\n")
            return

        # Affiche un message indiquant le début du scan
        self.result_text.insert(tk.END, f"Balayage de ports sur {target_ip}...\n")

        # Lance un thread pour exécuter le scan des ports
        threading.Thread(target=self.scan_ports, args=(target_ip, start_port, end_port)).start()

    def scan_ports(self, target_ip, start_port, end_port):
        start_time = datetime.now()  # Enregistre l'heure de début du scan
        open_ports = []  # Liste pour stocker les ports ouverts
        closed_ports = []  # Liste pour stocker les ports fermés
        threads = []  # Liste pour stocker les threads

        # Boucle pour scanner chaque port dans la plage spécifiée
        for port in range(start_port, end_port + 1):
            # Crée un thread pour scanner chaque port
            thread = threading.Thread(target=self.scan_port, args=(target_ip, port, open_ports, closed_ports))
            thread.start()  # Démarre le thread
            threads.append(thread)  # Ajoute le thread à la liste

        # Attend que tous les threads se terminent
        for thread in threads:
            thread.join()

        # Affiche les résultats du scan
        for port in open_ports:
            self.result_text.insert(tk.END, f"{datetime.now()} Le port {port} : OUVERT\n")
        for port in closed_ports:
            self.result_text.insert(tk.END, f"{datetime.now()} Le port {port} : FERMÉ\n")

        end_time = datetime.now()  # Enregistre l'heure de fin du scan
        self.result_text.insert(tk.END, f"Balayage terminé en {end_time - start_time}\n")

    def scan_port(self, target_ip, port, open_ports, closed_ports):
        try:
            # Crée un objet socket et tente de se connecter au port spécifié
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)  # Définit une durée maximale d'attente pour la connexion
            result = s.connect_ex((target_ip, port))  # Teste la connexion au port
            if result == 0:
                open_ports.append(port)  # Ajoute le port à la liste des ports ouverts
            else:
                closed_ports.append(port)  # Ajoute le port à la liste des ports fermés
            s.close()  # Ferme la connexion
        except Exception as e:
            # Affiche un message en cas d'erreur lors de la numérisation du port
            self.result_text.insert(tk.END, f"Erreur lors de la numérisation du port {port}: {e}\n")

if __name__ == "__main__":
    # Crée une instance de l'application et lance la boucle principale
    app = PortScannerApp()
    app.mainloop()
