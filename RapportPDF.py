from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_cover(title, logo_path, output_path):
    # Créer un nouveau canvas avec la taille de la page letter
    c = canvas.Canvas(output_path, pagesize=letter)

    # Ajouter le logo
    c.drawImage(logo_path, x=100, y=500, width=200, height=200)

    # Ajouter le titre
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(400, 300, title)

    # Sauvegarder le document
    c.save()

# Appeler la fonction avec les informations nécessaires
title = "Mise en couverture"
logo_path = "C:/Users/aelhocine/Documents/Master CyberSécurité/Projet Cybersécurité (TOOLBOX)/Projet-Toolbox/Logo-entreprise.png"
output_path = "./output/cover.pdf"
create_cover(title, logo_path, output_path)
