import requests  # Importe le module requests pour envoyer des requêtes HTTP.
import re  # Importe le module re pour les expressions régulières.
from bs4 import BeautifulSoup  # Importe la classe BeautifulSoup pour parser le HTML.
import webbrowser  # Importe le module webbrowser pour ouvrir des URLs dans un navigateur.
import tkinter as tk  # Importe le module tkinter pour créer une interface graphique.
from tkinter import ttk  # Importe les éléments de style ttk (themed tk) de tkinter.
from urllib.parse import urljoin  # Importe la fonction urljoin pour résoudre les URLs relatives.

# Définit la fonction scan_website(url) pour scanner un site web à partir de l'URL donnée.
def scan_website(url):
    # Step 1: Discover URLs on the website
    # Découvre les URLs sur le site web.
    discovered_urls = discover_urls(url)
    vulnerabilities_found = []  # Initialise une liste pour stocker les vulnérabilités trouvées.

    # Step 2: Scan discovered URLs for vulnerabilities
    # Parcourt les URLs découvertes pour rechercher des vulnérabilités.
    for page_url in discovered_urls:
        vulnerabilities = scan_url(page_url)
        if vulnerabilities:
            vulnerabilities_found.append((page_url, vulnerabilities))

    return vulnerabilities_found  # Retourne les vulnérabilités trouvées.

# Définit la fonction discover_urls(url) pour découvrir les URLs sur un site web.
def discover_urls(url):
    discovered_urls = []  # Initialise une liste pour stocker les URLs découvertes.

    # Send a GET request to the given URL
    # Envoie une requête GET à l'URL donnée.
    response = requests.get(url, allow_redirects=False)
    if response.status_code == 200:  # Si la réponse est OK (status code 200).
        # Parse the HTML content of the response
        # Parse le contenu HTML de la réponse.
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all anchor tags and extract URLs
        # Trouve toutes les balises ancre et extrait les URLs.
        for anchor_tag in soup.find_all("a"):  # Parcourt toutes les balises 'a'.
            href = anchor_tag.get("href")  # Obtient la valeur de l'attribut 'href'.
            if href:  # Si l'URL n'est pas vide.
                absolute_url = urljoin(url, href)  # Résout l'URL absolue.
                discovered_urls.append(absolute_url)  # Ajoute l'URL à la liste des URLs découvertes.

    return discovered_urls  # Retourne les URLs découvertes.

# Définit la fonction scan_url(url) pour scanner une URL donnée à la recherche de vulnérabilités.
def scan_url(url):
    vulnerabilities = {}  # Initialise un dictionnaire pour stocker les vulnérabilités.

    # Example: Check for SQL injection vulnerability
    # Exemple : Vérifie la vulnérabilité à l'injection SQL.
    if is_sql_injection_vulnerable(url):
        vulnerabilities["SQL injection vulnerability"] = "Injecting SQL code into input fields"

    # Example: Check for cross-site scripting (XSS) vulnerability
    # Exemple : Vérifie la vulnérabilité au cross-site scripting (XSS).
    if is_xss_vulnerable(url):
        vulnerabilities["Cross-site scripting (XSS) vulnerability"] = "Injecting malicious scripts into input fields"

    return vulnerabilities  # Retourne les vulnérabilités trouvées.

# Définit la fonction is_sql_injection_vulnerable(url) pour vérifier si une URL est vulnérable à l'injection SQL.
def is_sql_injection_vulnerable(url):
    # Perform checks for SQL injection vulnerability
    # Effectue des vérifications pour la vulnérabilité à l'injection SQL.
    # Exemple : Envoie une requête SQL malveillante et vérifie la réponse.
    payload = "' OR '1'='1"
    response = requests.get(url + "?id=" + payload, allow_redirects=False)
    if re.search(r"error|warning", response.text, re.IGNORECASE):  # Si les mots "error" ou "warning" sont présents dans la réponse.
        return True  # La vulnérabilité est détectée.
    return False  # Sinon, la vulnérabilité n'est pas détectée.

# Définit la fonction is_xss_vulnerable(url) pour vérifier si une URL est vulnérable au cross-site scripting (XSS).
def is_xss_vulnerable(url):
    # Perform checks for cross-site scripting (XSS) vulnerability
    # Effectue des vérifications pour la vulnérabilité au cross-site scripting (XSS).
    # Exemple : Injecte une balise de script et vérifie si elle est exécutée.
    payload = "<script>alert('XSS')</script>"
    response = requests.get(url + "?input=" + payload, allow_redirects=False)
    if payload in response.text:  # Si la charge utile est présente dans la réponse.
        return True  # La vulnérabilité est détectée.
    return False  # Sinon, la vulnérabilité n'est pas détectée.

# Définit la fonction start_scan() pour démarrer le scan lorsque le bouton est cliqué.
def start_scan():
    url = url_entry.get()  # Obtient l'URL à partir de l'entrée utilisateur.
    scan_results.delete("1.0", tk.END)  # Efface les résultats précédents dans la zone de texte.

    vulnerabilities_found = scan_website(url)  # Scanne le site web pour les vulnérabilités.
    if vulnerabilities_found:  # Si des vulnérabilités sont trouvées.
        scan_results.insert(tk.END, "Vulnerabilities found:\n")  # Affiche un en-tête.
        for page_url, vulnerabilities in vulnerabilities_found:  # Parcourt les vulnérabilités trouvées.
            scan_results.insert(tk.END, f"\nURL: {page_url}\n")  # Affiche l'URL de la page.
            for vulnerability, attack_method in vulnerabilities.items():  # Parcourt les vulnérabilités spécifiques.
                scan_results.insert(tk.END, f"Vulnerability: {vulnerability}\n")  # Affiche le type de vulnérabilité.
                scan_results.insert(tk.END, f"Attack Method: {attack_method}\n")  # Affiche la méthode d'attaque.
    else:  # Si aucune vulnérabilité n'est trouvée.
        scan_results.insert(tk.END, "No vulnerabilities found.")  # Affiche un message indiquant qu'aucune vulnérabilité n'a été trouvée.

# Crée une fenêtre tkinter pour l'interface graphique.
root = tk.Tk()
root.title("Website Vulnerability Scanner")  # Définit le titre de la fenêtre.

main_frame = ttk.Frame(root, padding="10")  # Crée un cadre principal avec un espacement de 10 pixels.
main_frame.grid(column=0, row=0)  # Place le cadre principal dans la grille.

url_label = ttk.Label(main_frame, text="Enter URL:")  # Crée une étiquette pour indiquer où saisir l'URL.
url_label.grid(column=1, row=1, sticky=tk.W)  # Place l'étiquette dans la grille.

url_entry = ttk.Entry(main_frame, width=40)  # Crée un champ de saisie pour l'URL.
url_entry.grid(column=2, row=1, sticky=tk.E)  # Place le champ de saisie dans la grille.

scan_button = ttk.Button(main_frame, text="Start Scan", command=start_scan)  # Crée un bouton pour démarrer le scan.
scan_button.grid(column=3, row=1)  # Place le bouton dans la grille.

scan_results = tk.Text(main_frame, height=20, width=80, font=("Courier", 12))  # Crée une zone de texte pour afficher les résultats du scan.
scan_results.grid(column=1, row=2, columnspan=3)  # Place la zone de texte dans la grille.

root.mainloop()  # Lance la boucle principale de l'interface graphique.
