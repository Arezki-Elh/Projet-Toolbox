import tkinter as tk

def search_cve(search_term):
    results_text.delete(1.0, tk.END)
    with open(r'C:\Users\aelhocine\Documents\Master CyberSécurité\Projet Cybersécurité (TOOLBOX)\Projet-Toolbox\allitems.txt', encoding='utf-8', errors='ignore') as file:
        cve_data = file.read()
        cves = cve_data.split('======================================================')
        found = False
        for cve in cves:
            if search_term.lower() in cve.lower():
                results_text.insert(tk.END, cve + '\n' + '='*50 + '\n')
                found = True
        if not found:
            results_text.insert(tk.END, "Aucune CVE correspondante trouvée pour '{}'\n".format(search_term))

def perform_search():
    search_term = entry.get()
    search_cve(search_term)

# Création de la fenêtre principale
root = tk.Tk()
root.title("Recherche de CVE")

# Cadre pour entrer le terme de recherche
entry_frame = tk.Frame(root)
entry_frame.pack(pady=10)

search_label = tk.Label(entry_frame, text="Entrez le terme de recherche :")
search_label.pack(side=tk.LEFT)

entry = tk.Entry(entry_frame, width=30)
entry.pack(side=tk.LEFT)

search_button = tk.Button(entry_frame, text="Rechercher", command=perform_search)
search_button.pack(side=tk.LEFT)

# Cadre pour afficher les résultats
results_frame = tk.Frame(root)
results_frame.pack(padx=10, pady=10)

results_text = tk.Text(results_frame, width=80, height=20)
results_text.pack()

# Exécuter la boucle principale
root.mainloop()
