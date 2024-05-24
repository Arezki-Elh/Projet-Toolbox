import tkinter as tk  # Importation de la bibliothèque tkinter pour créer l'interface graphique
from tkinter import ttk  # Importation du module ttk pour utiliser les widgets de style
import subprocess  # Importation du module subprocess pour exécuter des processus externes

class ConfigToolbox(tk.Tk):  # Définition de la classe ConfigToolbox héritant de la classe tk.Tk
    def __init__(self):  # Définition de la méthode __init__ pour initialiser l'objet
        super().__init__()  # Appel du constructeur de la classe parente
        self.title("Configuration de la Toolbox")  # Définition du titre de la fenêtre
        self.geometry("400x300")  # Définition de la taille de la fenêtre

        # Création des widgets
        self.create_widgets()

    def create_widgets(self):  # Définition de la méthode pour créer les widgets
        # Création des widgets de configuration
        self.create_configuration_widgets()

        # Création du bouton pour exécuter le script sélectionné
        run_button = ttk.Button(self, text="Exécuter le script sélectionné", command=self.run_selected_script)
        run_button.pack(pady=10)  # Placement du bouton avec un espace de 10 pixels en dessous

    def create_configuration_widgets(self):  # Définition de la méthode pour créer les widgets de configuration
        # Chargement de l'image de fond
        self.background_image = tk.PhotoImage(file="./fond-toolbox.png")
        self.canvas = tk.Canvas(self, width=self.background_image.width(), height=self.background_image.height())
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")

        # Définition des dimensions des éléments
        element_width = 200
        element_height = 30
        x_offset = (self.background_image.width() - element_width * 2) // 2
        y_offset = 50

        # Étiquette et liste déroulante pour le nom de l'entreprise
        company_name_label = ttk.Label(self.canvas, text="Nom de l'entreprise :")
        company_name_label.place(x=x_offset, y=100 + y_offset)
        self.company_name_var = tk.StringVar()
        company_name_combobox = ttk.Combobox(self.canvas, textvariable=self.company_name_var,
                                             values=["Entreprise A", "Entreprise B", "Entreprise C", "Entreprise D", "Mairie de Romainville"])
        company_name_combobox.place(x=x_offset + element_width + 10, y=100 + y_offset)

        # Étiquette et liste déroulante pour le script à exécuter
        script_label = ttk.Label(self.canvas, text="Script à exécuter :")
        script_label.place(x=x_offset, y=150 + y_offset)
        self.script_var = tk.StringVar()
        script_combobox = ttk.Combobox(self.canvas, textvariable=self.script_var, values=[
            "nmap.py",
            "SQLinjection.py",
            "Brutforcessh.py",
            "arpscanner.py",
            "keylogsite.py",
            "vulni-scan.py",
            "john-crack.py"
        ])
        script_combobox.place(x=x_offset + element_width + 10, y=150 + y_offset)

    def run_selected_script(self):  # Définition de la méthode pour exécuter le script sélectionné
        # Chemins des scripts correspondant aux noms de script sélectionnés
        script_paths = {
            "nmap.py": "./nmap.py",
            "SQLinjection.py": "./SQLinjection.py",
            "Brutforcessh.py": "./Brutforcessh.py",
            "arpscanner.py": "./arpscanner.py",
            "keylogsite.py": "./keylogsite.py",
            "vulni-scan.py": "./vulni-scan.py",
            "john-crack.py": "./john-crack.py"
        }
        script_name = self.script_var.get()  # Récupération du nom de script sélectionné
        script_path = script_paths.get(script_name)  # Récupération du chemin du script

        # Si un chemin de script est trouvé, exécuter le script
        if script_path:
            subprocess.Popen(["python", script_path])
        else:
            print("Aucun script n'est disponible pour le script sélectionné.")

if __name__ == "__main__":  # Condition pour exécuter le programme si ce fichier est exécuté directement
    app = ConfigToolbox()  # Création d'une instance de la classe ConfigToolbox
    app.mainloop()  # Lancement de la boucle principale de l'interface graphique
