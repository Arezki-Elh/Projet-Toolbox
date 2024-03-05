import tkinter as tk
from tkinter import ttk

class ConfigToolbox(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Configuration de la Toolbox")
        self.geometry("500x400")  # Augmentation de la taille de la fenêtre

        self.label = ttk.Label(self, text="Bienvenue dans la configuration de la Toolbox")
        self.label.pack(pady=10)

        # Choix prédéfinis pour le nom de l'entreprise
        self.company_names = ["Entreprise A", "Entreprise B", "Entreprise C", "Entreprise D", "Mairie de Romainville"]

        self.company_name_label = ttk.Label(self, text="Nom de l'entreprise :")
        self.company_name_label.pack()
        self.company_name_var = tk.StringVar()
        self.company_name_combobox = ttk.Combobox(self, textvariable=self.company_name_var, values=self.company_names)
        self.company_name_combobox.pack()

        # Choix prédéfinis pour le type de test
        self.test_types = [
            "1. Découverte de ports et de services",
            "2. Détection de vulnérabilités",
            "3. Analyse de la sécurité des mots de passe",
            "4. Tests d'authentification",
            "5. Exploitation de vulnérabilités",
            "6. Post-exploitation",
            "7. Reporting"
        ]

        self.test_type_label = ttk.Label(self, text="Type de test :")
        self.test_type_label.pack()
        self.test_type_var = tk.StringVar()
        self.test_type_combobox = ttk.Combobox(self, textvariable=self.test_type_var, values=self.test_types)
        self.test_type_combobox.pack()

        self.submit_button = ttk.Button(self, text="Valider", command=self.save_configuration)
        self.submit_button.pack(pady=20)

    def save_configuration(self):
        company_name = self.company_name_var.get()
        test_type = self.test_type_var.get()

        # Enregistrer la configuration dans un fichier JSON ou YAML
        # Exemple : {"company_name": company_name, "test_type": test_type}

        self.destroy()
        print("Configuration enregistrée avec succès.")

if __name__ == "__main__":
    app = ConfigToolbox()
    app.mainloop()
