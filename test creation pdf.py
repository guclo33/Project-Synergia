import os
import requests
from openai import OpenAI
from openai.types import Completion, CompletionChoice, CompletionUsage
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import textwrap

nom = "Test, Test"

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def generateur_texte(system_prompt, user_prompt1, assistant_prompt, prompt):
    response=client.chat.completions.create(model= "gpt-3.5-turbo", 
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt1}, 
            {"role": "assistant", "content": assistant_prompt},
            {"role": "user", "content": prompt}], 
        max_tokens = 500)
    return response
    


#SECTION MOTIVATIONS

motivation_system = "tu es un expert du modèle DISC Marston"

motivation_user = "décris-moi quelqu'un de prédominance rouge"

motivation_assistant= "Il s'agit de quelqu'un avec de fort ambition et un désir d'atteindre ses objectifs"

motivation_prompt= f"pour {nom} décris-moi quelqu'un de jaune"

motivation = generateur_texte(motivation_system, motivation_user, motivation_assistant, motivation_prompt)

motivation_text = motivation.choices[0].message.content

def generate_unique_filename(base_filename, extension= ".pdf"):
    counter = 1
    filename = base_filename + extension
    while os.path.exists(filename):
        filename = f"{base_filename}_{counter}{extension}"
        counter += 1
    return filename


def generate_simple_pdf(file_path, text_content):
    # Créer un objet canvas pour le fichier PDF
    unique_file_path = generate_unique_filename(file_path)
    
    c = canvas.Canvas(unique_file_path, pagesize=letter)
    
    
    # Spécifier la taille de la page (lettre américaine)
    width, height = letter
    margin_left = 50
    margin_right = 50
    margin_top = height - 50
    margin_bottom = 50
    text_width = width - margin_left - margin_right
    
    # Utiliser textwrap pour gérer les retours à la ligne
    wrapper = textwrap.TextWrapper(width=round(text_width / 6))  # Ajuster le ratio en fonction de la taille de la police
    wrapped_text = wrapper.fill(text_content)
    
    # Définir la position de départ du texte
    text_object = c.beginText(50, height - 50)  # Départ à 50 points du bord gauche et du haut
    
    # Définir la police et la taille du texte
    text_object.setFont("Helvetica", 12)
    
    # Ajouter chaque ligne au canevas
    for line in wrapped_text.splitlines():
        text_object.textLine(line)
    
    # Dessiner le texte sur le canvas
    c.drawText(text_object)
    
    # Terminer la page et sauvegarder le PDF
    c.showPage()
    c.save()
    

x = nom

# Chemin du nouveau dossier à créer
nouveau_dossier = f"C:/Users/Guillaume Cloutier/OneDrive/Synergia/{x}"

if not os.path.exists(nouveau_dossier):
    os.makedirs(nouveau_dossier) 
else:
    None
    

generate_simple_pdf(f"C:/Users/Guillaume Cloutier/OneDrive/Synergia/{x}/{x}", motivation_text)
