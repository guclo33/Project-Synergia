import os
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
from openai import OpenAI
from openai.types import Completion, CompletionChoice, CompletionUsage
from reportlab.lib.pagesizes import letter
from docx import Document
import textwrap

nom = "Evan, Cloutier"

#DONNÉES EXCEL

#Pour le client
synergia = pd.read_excel("C:/Users/Guillaume Cloutier/OneDrive/Synergia/Synergia.xlsx", sheet_name="Réponses 3")

synergia_nom = pd.DataFrame(synergia.loc[synergia["Nom"]== nom])

plage_nom = synergia_nom.iloc[:,2]
plage_questions1_11 = synergia_nom.iloc[:,6:49]
plage_questions17_20 = synergia_nom.iloc[:,62:77]
plage_questions1_20 = synergia_nom.iloc[:,6:77]

synergia_section1= pd.concat([plage_nom, plage_questions1_11, plage_questions17_20], axis=1)

synergia_section1_transposed = synergia_section1.transpose()

synergia_section1_string = synergia_section1_transposed.to_string(header=False)

synergia_section2 = pd.concat([plage_nom, plage_questions1_20], axis = 1)

synergia_section2_transposed = synergia_section2.transpose()

synergia_section2_string = synergia_section2_transposed.to_string(header=False)

#Pour le model 1

synergia_model1 = synergia.iloc[[92]]

plage_model1 = synergia_model1.iloc[:,2]
plage_model1_questions1_11 = synergia_model1.iloc[:,6:49]
plage_model1_questions17_20 = synergia_model1.iloc[:,62:77]

synergia_model1_section1= pd.concat([plage_model1, plage_model1_questions1_11, plage_model1_questions17_20], axis=1)

synergia_model1_section1_transposed = synergia_model1_section1.transpose()

synergia_model1_section1_string = synergia_model1_section1_transposed.to_string(header=False)

#Pour le model 2

synergia_model2 = synergia.iloc[[88]]

plage_model2 = synergia_model2.iloc[:,2]
plage_model2_questions1_11 = synergia_model2.iloc[:,6:49]
plage_model2_questions17_20 = synergia_model2.iloc[:,62:77]

synergia_model2_section1= pd.concat([plage_model2, plage_model2_questions1_11, plage_model2_questions17_20], axis=1)

synergia_model2_section1_transposed = synergia_model2_section1.transpose()

synergia_model2_section1_string = synergia_model2_section1_transposed.to_string(header=False)



#***VARIABLES ET FONCTIONS***


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def generateur_texte(message, token):
    response=client.chat.completions.create(model= "gpt-4o", 
        messages = message, 
        max_tokens = token)
    return response
    

# GÉNÉRER UN TEXTE POUR CHAQUE SECTION

#SECTION "EN BREF":

bref_system = "Je souhaite que tu crées un résumé de personnalité qui capte les aspects essentiels d'une personne, basé sur ses réponses à un questionnaire DISC et ses caractéristiques personnelles. Je t'envoie un format ou la première ligne est le nom et les suivantes sont les questions posées ainsi qu'un choix de réponse, les valeurs correspondent à une échelle de 0 à 10. Si c'est 0, ça ne représente pas la personne et 10 représente beacuoup la personne . Les valeurs \"moins que moi\" équivalent à 0 et \"plus que moi\" équivalent à 10. Le texte doit comprendre trois à quatre paragraphes, chacun se concentrant sur différents aspects de la personnalité de la personne : ses forces principales, sa manière de travailler, ses interactions sociales, et ses valeurs ou préférences. Inclut les forces dominantes comme le leadership, l'analytique, la créativité, ou l'organisation. Décris comment cette personne aborde son travail, en mettant en avant des aspects tels que la méthodicité, la rigueur, l'innovation, ou la flexibilité. Explique comment cette personne interagit avec les autres, que ce soit par son charisme, son écoute, ou sa bienveillance. Mentionne ses valeurs et préférences, telles que la recherche de qualité, la stabilité, la spontanéité, ou l'impact sur les autres. Adopte un ton positif et valorisant, en utilisant un langage riche et nuancé pour refléter les particularités de la personne. Assure-toi que chaque phrase soit unique et ajoute une touche de sophistication au texte. Assure-toi que le texte soit fluide, sans répétitions, et qu'il donne une vision claire et engageante de la personnalité."

bref_user = f"On va faire un test. Dans un texte de **MAXIMUM DE 220 MOTS**, voici les réponses aux questions de Madame test:/n {synergia_model1_section1_string}"

bref_assistant= "Marie-Soleil est une personne déterminée et audacieuse, qui utilise son indépendance et sa confiance en elle pour relever les défis avec assurance. Elle excelle dans la prise de décisions rapides et directes, grâce à son esprit stratégique et son sens de l'initiative, ce qui fait d'elle une leader naturelle./n Sa spontanéité et son approche positive, alliées à une ouverture d'esprit, lui permettent de s'adapter aisément aux imprévus. Motivée par des objectifs ambitieux, elle n'hésite pas à se lancer dans l'inconnu avec assurance. Bien qu'elle soit orientée vers l'action et l'efficacité, elle sait captiver les autres par son esprit divertissant et rendre chaque moment plus engageant./n Dans ses interactions sociales, Marie-Soleil est sociable et apprécie rencontrer de nouvelles personnes. Même si elle privilégie une communication directe, elle fait preuve de compassion, même si elle reste concentrée sur ses propres objectifs. Sa nature passionnée et spontanée fait d'elle une personne dynamique, capable d'inspirer son entourage et d'encourager des discussions stimulantes./n En somme, Marie-Soleil est une personne énergique et stratégiquement orientée, qui vise l'excellence tout en maintenant une grande adaptabilité dans ses actions."

bref_user2= f"Voici un deuxième exemple de Monsieur test. Dans un texte de **MAXIMUM DE 220 MOTS**, voici le questionnaire:/n {synergia_model2_section1_string}"

bref_assistant2= "Guillaume est une personne méthodique et analytique, guidée par un désir de comprendre les choses en détail et de s'assurer que tout suit un ordre logique. Son approche structurée et son attention aux détails font de lui un professionnel organisé, capable de garantir des résultats d'excellence. Il vise des standards élevés et cherche constamment à perfectionner son travail./n Sa prudence et son analyse réfléchie des situations montrent sa capacité à évaluer les options avant de prendre des décisions. Bien qu'il préfère analyser les données plutôt que d'agir sur des impulsions, il est déterminé à atteindre ses objectifs une fois sa décision prise. Cette rigueur est renforcée par une grande patience et une tolérance pour les situations complexes, lui permettant de persévérer même dans les environnements exigeants./n Dans ses interactions sociales, Guillaume est plus réservé, préférant se concentrer sur les faits concrets plutôt que sur les discussions superficielles. Il valorise le tact et la bienveillance dans ses relations, mais est avant tout motivé par le besoin d'assurer une qualité irréprochable dans tout ce qu'il fait. Sa capacité à évaluer l'impact de ses actions sur les autres montre un souci de préserver l'équilibre./n En somme, Guillaume est une personne rigoureuse, organisée et analytique, engagée à atteindre des résultats de haute qualité tout en maintenant une approche réfléchie et structurée."

bref_prompt= f"Maintenant, voici le véritable questionnaire qui nous servira pour toute la suite de la conversation. Execute la même tâche que les deux exemples précédents pour le questionnaire suivant:/n {synergia_section1_string}"

message_data= [{"role": "system",
               "content": bref_system},
               {"role": "user",
               "content": bref_user},
               {"role": "assistant",
               "content": bref_assistant},
               {"role": "user",
               "content": bref_user2},
               {"role": "assistant",
               "content": bref_assistant2},
               {"role": "user",
               "content": bref_prompt,}]

bref = generateur_texte(message_data, 400)

bref_text = bref.choices[0].message.content

#Section "Tes forces mises en lumière"

forces_prompt = "Je souhaite que tu identifies et présentes les 5 principales forces de cette même personne dans un texte de **MAXIMUM DE 150 MOTS**, basées sur son questionnaire, sous forme de points clés. Présente chaque force sous la forme d'une phrase concise accompagnée d'une icône représentative (comme un emoji) au début de chaque point. Adopte un ton positif et valorisant, en utilisant un langage précis et professionnel. Assure-toi que chaque point soit clair, succinct, et reflète les compétences de la personne. Voici un exemple de ce que je souhaite obtenir : [exemple 1 💡 Audace et Prise de Risques : Madame Test se distingue par sa capacité à prendre des risques calculés, n'hésitant pas à foncer vers l'inconnu avec une confiance remarquable.🎯 Orientation Vers les Objectifs : Sa détermination à atteindre des objectifs ambitieux la pousse à agir rapidement et efficacement, en restant toujours concentrée sur les résultats à atteindre.💬 Communication Directe : Elle excelle dans l'art de communiquer de manière claire et directe, ce qui lui permet de naviguer avec assurance dans les interactions et les prises de décision.🌟 Flexibilité et Spontanéité : Madame Test sait s'adapter aux situations imprévues avec une grande spontanéité, transformant les défis en opportunités pour innover et avancer. 🚀 Autonomie et Initiative : Son indépendance lui permet de travailler de manière autonome, prenant des initiatives audacieuses pour mener ses projets à terme sans nécessiter de supervision constante./n Exemple 2 🧠 Pensée Analytique : Guillaume excelle dans l'analyse détaillée, capable de naviguer à travers des situations complexes pour identifier les solutions optimales. 🔍 Orientation vers la Précision : Il possède une attention remarquable aux détails, s'assurant que chaque aspect de son travail répond aux plus hauts standards de qualité. 📈 Capacité de Planification Stratégique : Son aptitude à anticiper et à élaborer des stratégies à long terme démontre sa vision et sa capacité à orienter efficacement les ressources vers des objectifs définis. 🚀 Autonomie et Indépendance : Guillaume travaille efficacement de manière autonome, prenant des initiatives et conduisant des projets à leur terme avec peu de supervision. 🌱 Apprentissage Continu et Développement Personnel : Il est constamment en quête de croissance, cherchant à élargir ses connaissances et à perfectionner ses compétences pour s'adapter et innover.]. Assure-toi que les forces mises en avant soient directement liées aux caractéristiques clés de la personne et qu'elles reflètent une image positive et professionnelle."

message_data.append( 
  {
    "role": "assistant", 
    "content": bref_text
  }
)
  
message_data.append(
    {
        "role": "user",
        "content": forces_prompt
    }
)

forces = generateur_texte(message_data, 300)

forces_text = forces.choices[0].message.content


full_text= "En Bref\n" + bref_text + "\n\n" + "Forces et faiblesse\n" + forces_text


#def generate_unique_filename(base_filename, extension= ".pdf"):
    #counter = 1
    #filename = base_filename + extension
    #while os.path.exists(filename):
        #filename = f"{base_filename}_{counter}{extension}"
        #counter += 1
    #return filename


#def generate_simple_pdf(file_path, text_content):
    # Créer un objet canvas pour le fichier PDF
    #unique_file_path = generate_unique_filename(file_path)
    
    #c = canvas.Canvas(unique_file_path, pagesize=letter)
    
    # Charger une police qui supporte les émojis
    #pdfmetrics.registerFont(TTFont('Segoe UI Emoji', 'NotoColorEmoji-Regular.ttf'))
    
    # Spécifier la taille de la page (lettre américaine)
    #width, height = letter
    #margin_left = 50
    #margin_right = 50
    #margin_top = height - 50
    #margin_bottom = 50
    #text_width = width - margin_left - margin_right
    
    # Utiliser textwrap pour gérer les retours à la ligne
    #wrapper = textwrap.TextWrapper(width=round(text_width / 6))  # Ajuster le ratio en fonction de la taille de la police
    #wrapped_text = wrapper.wrap(text_content)
    
    # Définir la position de départ du texte
    #text_object = c.beginText(50, height - 50)  # Départ à 50 points du bord gauche et du haut
    
    # Définir la police et la taille du texte
    #text_object.setFont("Segoe UI Emoji", 12)
    
    # Ajouter chaque ligne au canevas
    #for line in wrapped_text:
        #text_object.textLine(line)
    
    # Dessiner le texte sur le canvas
    #c.drawText(text_object)
    
    # Terminer la page et sauvegarder le PDF
    #c.showPage()
    #c.save()
    



# Chemin du nouveau dossier à créer
#nouveau_dossier = f"C:/Users/Guillaume Cloutier/OneDrive/Synergia/{nom}"

#if not os.path.exists(nouveau_dossier):
    #os.makedirs(nouveau_dossier) 
#else:
   # None
    

#generate_simple_pdf(f"C:/Users/Guillaume Cloutier/OneDrive/Synergia/{nom}/{nom}", full_text)


def generate_unique_filename(base_filename, extension=".docx"):
    counter = 1
    filename = base_filename + extension
    while os.path.exists(filename):
        filename = f"{base_filename}_{counter}{extension}"
        counter += 1
    return filename

def generate_simple_word(file_path, text_content):
    # Créer un document Word
    unique_file_path = generate_unique_filename(file_path)
    doc = Document()

    # Ajouter du texte au document
    for line in text_content.splitlines():
        doc.add_paragraph(line)
    
    # Sauvegarder le document
    doc.save(unique_file_path)

# Chemin du nouveau dossier à créer

nouveau_dossier = f"C:/Users/Guillaume Cloutier/OneDrive/Synergia/{nom}"

if not os.path.exists(nouveau_dossier):
    os.makedirs(nouveau_dossier)

# Générer le fichier Word
generate_simple_word(f"{nouveau_dossier}/{nom}", full_text)