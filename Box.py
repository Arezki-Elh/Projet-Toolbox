import tkinter as tk  # Importation de la bibliothèque tkinter pour créer l'interface graphique
from tkinter import ttk  # Importation du module ttk pour utiliser les widgets de style

class ConfigToolbox(tk.Tk):  # Définition de la classe ConfigToolbox héritant de la classe tk.Tk
    def __init__(self):  # Définition de la méthode __init__ pour initialiser l'objet
        super().__init__()  # Appel du constructeur de la classe parente
        self.title("Configuration de la Toolbox")  # Définition du titre de la fenêtre

        # Chargement de l'image de fond depuis le fichier spécifié
        self.background_image = tk.PhotoImage(file="C:/Users/aelhocine/Documents/fond-toolbox.png")

        # Définition des dimensions de la fenêtre en fonction de l'image de fond
        self.geometry(f"{self.background_image.width()}x{self.background_image.height()}")

        # Création d'un canevas avec l'image de fond
        self.canvas = tk.Canvas(self, width=self.background_image.width(), height=self.background_image.height())
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")

        # Définition des dimensions des éléments
        element_width = 200
        element_height = 30

        # Calcul des positions pour centrer les éléments horizontalement
        x_offset = (self.background_image.width() - element_width * 2) // 2
        y_offset = 50

        # Création de l'étiquette et de la liste déroulante pour le nom de l'entreprise
        company_name_label = ttk.Label(self.canvas, text="Nom de l'entreprise :")
        company_name_label.place(x=x_offset, y=100 + y_offset)  # Positionnement de l'étiquette
        self.company_name_var = tk.StringVar()  # Variable pour stocker le nom de l'entreprise sélectionné
        company_name_combobox = ttk.Combobox(self.canvas, textvariable=self.company_name_var, values=["Entreprise A", "Entreprise B", "Entreprise C", "Entreprise D", "Mairie de Romainville"])
        company_name_combobox.place(x=x_offset + element_width + 10, y=100 + y_offset)  # Positionnement de la liste déroulante

        # Création de l'étiquette et de la liste déroulante pour le type de test
        test_type_label = ttk.Label(self.canvas, text="Type de test :")
        test_type_label.place(x=x_offset, y=150 + y_offset)  # Positionnement de l'étiquette
        self.test_type_var = tk.StringVar()  # Variable pour stocker le type de test sélectionné
        test_type_combobox = ttk.Combobox(self.canvas, textvariable=self.test_type_var, values=[
            "Découverte de ports et de services",
            "Détection de vulnérabilités",
            "Analyse de la sécurité des mots de passe",
            "Tests d'authentification",
            "Exploitation de vulnérabilités",
            "Post-exploitation",
            "Reporting"
        ])
        test_type_combobox.place(x=x_offset + element_width + 10, y=150 + y_offset)  # Positionnement de la liste déroulante

        # Création du bouton "Valider" et définition de sa position
        submit_button = ttk.Button(self.canvas, text="Valider", command=self.save_configuration)
        submit_button.place(x=(self.background_image.width() - element_width) // 2, y=self.background_image.height() - 100)

    def save_configuration(self):  # Définition de la méthode pour enregistrer la configuration
        company_name = self.company_name_var.get()  # Récupération du nom de l'entreprise sélectionné
        test_type = self.test_type_var.get()  # Récupération du type de test sélectionné

        # Enregistrement de la configuration dans un fichier JSON ou YAML

        self.destroy()  # Fermeture de la fenêtre
        print("Configuration enregistrée avec succès.")  # Affichage d'un message de confirmation

if __name__ == "__main__":  # Condition pour exécuter le programme si ce fichier est exécuté directement
    app = ConfigToolbox()  # Création d'une instance de la classe ConfigToolbox
    app.mainloop()  # Lancement de la boucle principale de l'interface graphique
