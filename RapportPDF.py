# Importer les modules nécessaires de ReportLab
from reportlab.lib.pagesizes import letter  # Importer la taille de page standard pour le document PDF
from reportlab.lib import colors  # Importer les couleurs
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle  # Importer les styles de paragraphe
from reportlab.lib.units import inch  # Importer les unités de mesure en pouces
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image  # Importer les éléments de base pour créer le PDF

def create_cover(title, logo_path, output_path):
    # Définir le style pour le titre
    styles = getSampleStyleSheet()
    title_style = styles["Title"]  # Obtenir le style de titre prédéfini
    title_style.alignment = 1  # Alignement au centre

    # Créer le document PDF
    doc = SimpleDocTemplate(output_path, pagesize=letter)  # Créer un objet de document PDF avec une taille de page lettre
    content = []  # Initialiser une liste pour contenir le contenu du PDF

    # Ajouter le logo de l'entreprise en haut de page
    logo = Image(logo_path, width=2*inch, height=2*inch)  # Créer un objet image avec le chemin d'accès au logo
    logo.hAlign = "CENTER"  # Aligner le logo au centre horizontalement
    content.append(logo)  # Ajouter le logo à la liste de contenu

    # Ajouter un espace
    content.append(Spacer(1, 0.5*inch))  # Ajouter un espace vertical de 0.5 pouce

    # Ajouter le titre
    title_text = "<br/><br/><br/><br/>" + title + "<br/><br/><br/>"  # Texte de titre avec des balises HTML pour l'espacement
    title_paragraph = Paragraph(title_text, title_style)  # Créer un paragraphe avec le texte de titre et le style de titre
    content.append(title_paragraph)  # Ajouter le paragraphe de titre à la liste de contenu

    # Construire le PDF
    doc.build(content)  # Construire le document PDF avec le contenu spécifié

# Appeler la fonction avec les informations nécessaires
title = "Mise en couverture"  # Titre du document PDF
logo_path = "C:/Users/aelhocine/Documents/Master CyberSécurité/Projet Cybersécurité (TOOLBOX)/Projet-Toolbox/Logo-entreprise.png"  # Chemin d'accès au logo de l'entreprise
output_path = "output/cover.pdf"  # Chemin d'accès pour enregistrer le fichier PDF de couverture
create_cover(title, logo_path, output_path)  # Appeler la fonction pour créer la couverture du PDF
