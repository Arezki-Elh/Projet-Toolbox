# Import des modules nécessaires
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import scapy.all as scapy
import re

# Fonction pour envoyer une requête ARP à une plage d'adresses IP spécifiée
def send_arp_request(ip_range, result_text):
    # Envoi d'une requête ARP à la plage d'adresses IP spécifiée
    arp_result = scapy.arping(ip_range, verbose=False)
    # Accès aux résultats dans le tuple retourné
    answered_list = arp_result[0]
    # Création d'une liste de chaînes pour stocker les résultats formatés
    result_lines = []
    # Parcours de chaque réponse ARP
    for result in answered_list:
        # Récupération de l'adresse IP source et de l'adresse MAC source
        ip_src = result[1].psrc
        mac_src = result[1].hwsrc
        # Gestion du cas où le nom d'hôte n'est pas disponible
        hostname = result[1].hostname if hasattr(result[1], 'hostname') and result[1].hostname is not None else "Unknown"
        # Formatage de la ligne de résultat
        result_line = f"{ip_src} {mac_src} {hostname}"
        # Ajout de la ligne de résultat à la liste
        result_lines.append(result_line)
    # Conversion de la liste de chaînes en une seule chaîne avec des sauts de ligne
    result_str = "\n".join(result_lines)
    # Affichage des résultats dans la zone de texte des résultats
    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, result_str)
    result_text.config(state=tk.DISABLED)

# Création de la fenêtre principale
root = tk.Tk()
root.title("ARP Scanner")
root.geometry("800x600")

# Entête
header = tk.Label(root, text="ARP Scanner", font=("Arial", 16, "bold"))
header.pack(pady=10)

# Champ de saisie pour l'adresse IP et la plage
ip_range_label = tk.Label(root, text="Enter IP address range (e.g., 192.168.1.0/24):")
ip_range_label.pack()
ip_range_entry = tk.Entry(root, width=50)
ip_range_entry.pack()

# Bouton de scan
scan_button = tk.Button(root, text="Scan", command=lambda: send_arp_request(ip_range_entry.get(), result_text))
scan_button.pack(pady=10)

# Zone de texte pour afficher les résultats
result_text = ScrolledText(root, wrap=tk.WORD, width=80, height=20)
result_text.pack(padx=10, pady=10)

# Affichage de la fenêtre
root.mainloop()
