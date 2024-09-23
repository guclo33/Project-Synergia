import os
import time
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
pd.set_option('future.no_silent_downcasting', True)
from openai import OpenAI
from openai.types import Completion, CompletionChoice, CompletionUsage
from reportlab.lib.pagesizes import letter
import textwrap
from docx import Document



  
# *****À FAIRE**** code pour automatisation, activation lors de réception d'un nouveau formulaire 

#NOM format "Prénom, Nom"

nom = "Veillette, Joanie"

#DONNÉES EXCEL

#Pour le client
synergia = pd.read_excel("C:/Users/Guillaume Cloutier/OneDrive/Synergia/Synergia.xlsx", sheet_name="synergia_mlm")

synergia_model = pd.read_excel("C:/Users/Guillaume Cloutier/OneDrive/Synergia/Synergia.xlsx", sheet_name="Réponses 3")

synergia_nom = pd.DataFrame(synergia.loc[synergia["Nom"]== nom])


#plage de questions utilisé pour les prompts

plage_nom = synergia_nom.iloc[:,2:3]
plage_questions1_15 = synergia_nom.iloc[:,6:66]
plage_questions16_24 = synergia_nom.iloc[:,66:102]
plage_questions_developpement = synergia_nom.iloc[:,102:105]
plage_questionnaire_complet = synergia_nom.iloc[:,6:105]


#definition de la fonction pour formatter les résultats des bases de données
def excel_to_string(*args):
  return pd.concat(args, axis=1).transpose().to_string(header=False)



#section couleurs

synergia_couleur_string = excel_to_string(plage_nom, plage_questions1_15)


#section archétype

synergia_archetype_string = excel_to_string(plage_nom, plage_questions16_24)


#Questions développement


synergia_section_developpement_string = excel_to_string(plage_nom, plage_questions_developpement)


#Questionnaire complet

#synergia_complet_string = excel_to_string(plage_nom, plage_questionnaire_complet)

synergia_complet_string = synergia_couleur_string + "\n" +synergia_archetype_string+ "\n" + synergia_section_developpement_string

#Pour le model 1

synergia_model1 = synergia_model.iloc[[92]]

plage_model1 = synergia_model1.iloc[:,2]
plage_model1_questions1_11 = synergia_model1.iloc[:,6:50]
plage_model1_questions17_20 = synergia_model1.iloc[:,62:78]

synergia_model1_section1_string = excel_to_string(plage_model1, plage_model1_questions1_11, plage_model1_questions17_20)



#Pour le model 2

synergia_model2 = synergia_model.iloc[[88]]

plage_model2 = synergia_model2.iloc[:,2]
plage_model2_questions1_11 = synergia_model2.iloc[:,6:50]
plage_model2_questions17_20 = synergia_model2.iloc[:,62:78]

synergia_model2_section1_string = excel_to_string(plage_model2, plage_model2_questions1_11, plage_model2_questions17_20)


#***VARIABLES ET FONCTIONS***


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def generateur_texte(message, token):
    response=client.chat.completions.create(model= "gpt-4o", 
        messages = message, 
        max_tokens = token)
    return response
  
def context_append(assistant, user) :
  message_data.append( 
    {
      "role": "assistant", 
      "content": assistant
    }
  )
  message_data.append(
    {
        "role": "user",
        "content": user
    }
  )


    
#Pour avoir les pourcentage de Couleur et d'archétype

def moyenne(*colonnes):
    colonne = synergia_nom.iloc[:,list(colonnes)].replace({
        "Plus comme moi" : 10,
        "Moins comme moi" : 0
    }).infer_objects(copy=False)
    valeurs= colonne.to_numpy()
    return round(valeurs.mean()*10)

bleu = moyenne(6, 13, 17, 18, 24, 29, 30, 34, 41, 45, 49, 51, 57, 59, 64)
rouge = moyenne(7,12,14,19,22,27,31,35,39,44,48,50,55,61,65)
jaune = moyenne(8,10,15,21,23,26,32,36,40,42,46,52,56,60,62)
vert = moyenne(9,11,16,20,25,28,33,37,38,43,47,53,54,58,63)
explorateur = moyenne()
protecteur = moyenne()
bouffon = moyenne()
souverain = moyenne()
magicien = moyenne()
createur = moyenne()
hero = moyenne()
citoyen = moyenne()
sage = moyenne()
amant = moyenne()
rebelle = moyenne()
optimiste = moyenne()



# GÉNÉRER UN TEXTE POUR CHAQUE SECTION

#SECTION "EN BREF":

bref_system = "Je souhaite que tu crées un résumé de personnalité qui capte les aspects essentiels d'une personne, basé sur ses réponses à un questionnaire DISC et ses caractéristiques personnelles. Je t'envoie un format ou la première ligne est le nom et les suivantes sont les questions posées ainsi qu'un choix de réponse, les valeurs correspondent à une échelle de 0 à 10. Si c'est 0, ça ne représente pas la personne et 10 représente beacuoup la personne . Les valeurs \"moins que moi\" équivalent à 0 et \"plus que moi\" équivalent à 10. Le texte doit comprendre trois à quatre paragraphes, chacun se concentrant sur différents aspects de la personnalité de la personne : ses forces principales, sa manière de travailler, ses interactions sociales, et ses valeurs ou préférences. Inclut les forces dominantes comme le leadership, l'analytique, la créativité, ou l'organisation. Décris comment cette personne aborde son travail, en mettant en avant des aspects tels que la méthodicité, la rigueur, l'innovation, ou la flexibilité. Explique comment cette personne interagit avec les autres, que ce soit par son charisme, son écoute, ou sa bienveillance. Mentionne ses valeurs et préférences, telles que la recherche de qualité, la stabilité, la spontanéité, ou l'impact sur les autres. Adopte un ton positif et valorisant, en utilisant un langage riche et nuancé pour refléter les particularités de la personne. Assure-toi que chaque phrase soit unique et ajoute une touche de sophistication au texte. Assure-toi que le texte soit fluide, sans répétitions, et qu'il donne une vision claire et engageante de la personnalité."

bref_user = f"On va faire un test. Dans un texte de **MAXIMUM DE 220 MOTS**, voici les réponses aux questions de Madame test:\n {synergia_model1_section1_string}"

bref_assistant= "Marie-Soleil est une personne déterminée et audacieuse, qui utilise son indépendance et sa confiance en elle pour relever les défis avec assurance. Elle excelle dans la prise de décisions rapides et directes, grâce à son esprit stratégique et son sens de l'initiative, ce qui fait d'elle une leader naturelle.\n Sa spontanéité et son approche positive, alliées à une ouverture d'esprit, lui permettent de s'adapter aisément aux imprévus. Motivée par des objectifs ambitieux, elle n'hésite pas à se lancer dans l'inconnu avec assurance. Bien qu'elle soit orientée vers l'action et l'efficacité, elle sait captiver les autres par son esprit divertissant et rendre chaque moment plus engageant.\n Dans ses interactions sociales, Marie-Soleil est sociable et apprécie rencontrer de nouvelles personnes. Même si elle privilégie une communication directe, elle fait preuve de compassion, même si elle reste concentrée sur ses propres objectifs. Sa nature passionnée et spontanée fait d'elle une personne dynamique, capable d'inspirer son entourage et d'encourager des discussions stimulantes.\n En somme, Marie-Soleil est une personne énergique et stratégiquement orientée, qui vise l'excellence tout en maintenant une grande adaptabilité dans ses actions."

bref_user2= f"Voici un deuxième exemple de Monsieur test. Dans un texte de **MAXIMUM DE 220 MOTS**, voici le questionnaire:\n {synergia_model2_section1_string}"

bref_assistant2= "Guillaume est une personne méthodique et analytique, guidée par un désir de comprendre les choses en détail et de s'assurer que tout suit un ordre logique. Son approche structurée et son attention aux détails font de lui un professionnel organisé, capable de garantir des résultats d'excellence. Il vise des standards élevés et cherche constamment à perfectionner son travail.\n Sa prudence et son analyse réfléchie des situations montrent sa capacité à évaluer les options avant de prendre des décisions. Bien qu'il préfère analyser les données plutôt que d'agir sur des impulsions, il est déterminé à atteindre ses objectifs une fois sa décision prise. Cette rigueur est renforcée par une grande patience et une tolérance pour les situations complexes, lui permettant de persévérer même dans les environnements exigeants.\n Dans ses interactions sociales, Guillaume est plus réservé, préférant se concentrer sur les faits concrets plutôt que sur les discussions superficielles. Il valorise le tact et la bienveillance dans ses relations, mais est avant tout motivé par le besoin d'assurer une qualité irréprochable dans tout ce qu'il fait. Sa capacité à évaluer l'impact de ses actions sur les autres montre un souci de préserver l'équilibre.\n En somme, Guillaume est une personne rigoureuse, organisée et analytique, engagée à atteindre des résultats de haute qualité tout en maintenant une approche réfléchie et structurée."

bref_prompt= f"""Maintenant, voici le véritable questionnaire qui nous servira pour toute la suite de la conversation. Execute la même tâche que les deux exemples précédents dans un **MAXIMUM DE 200 MOTS** pour le questionnaire suivant:\n {synergia_complet_string}. Utilise principalement les réponses des questions 1 à 15 pour générer le résumé principal du profil. Mais intègre très subtilement les réponses des questions 16 à 24 afin d'ajouter un léger accent au profil, simplement en captant l’essence des motivations profondes de la personne mais sans que cette section ne prenne le dessus. Fais 3 paragraphes

À partir des questions 1 à 15, dis-moi quels serait les % disc de la personne. Exemple : Marie-Soleil est 85% rouge, 78% jaune, 30% verte et 28% bleu."""

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

bref = generateur_texte(message_data, 500)

bref_text = bref.choices[0].message.content

#Section "Tes forces mises en lumière"

forces_prompt = f"Je souhaite que tu identifies et présentes les 5 principales forces de cette même personne dans un texte de **MAXIMUM DE 150 MOTS** sous forme de points clés, basées sur ses couleurs de personalités ainsi que son questionnaire : {synergia_couleur_string}.\nPrésente chaque force sous la forme d'une phrase concise accompagnée d'une icône représentative (comme un emoji) au début de chaque point. Adopte un ton positif et valorisant, en utilisant un langage précis et professionnel. Assure-toi que chaque point soit clair, succinct, et reflète les compétences de la personne dans sa vie personnelle. Voici un exemple de ce que je souhaite obtenir : [exemple 1 💡 Audace et Prise de Risques : Madame Test se distingue par sa capacité à prendre des risques calculés, n'hésitant pas à foncer vers l'inconnu avec une confiance remarquable.🎯 Orientation Vers les Objectifs : Sa détermination à atteindre des objectifs ambitieux la pousse à agir rapidement et efficacement, en restant toujours concentrée sur les résultats à atteindre.💬 Communication Directe : Elle excelle dans l'art de communiquer de manière claire et directe, ce qui lui permet de naviguer avec assurance dans les interactions et les prises de décision.🌟 Flexibilité et Spontanéité : Madame Test sait s'adapter aux situations imprévues avec une grande spontanéité, transformant les défis en opportunités pour innover et avancer. 🚀 Autonomie et Initiative : Son indépendance lui permet de travailler de manière autonome, prenant des initiatives audacieuses pour mener ses projets à terme sans nécessiter de supervision constante.\n "


context_append(bref_text, forces_prompt)

forces = generateur_texte(message_data, 300)

forces_text = forces.choices[0].message.content

#Section "Tes défis Potentiels"

defis_prompt = "Je souhaite que tu identifies et présentes les 4 défis potentiels de cette personne dans sa vie personnelle basé sur ses couleurs de personnalité ainsi que sur son questionnaire des questions 1 à 15, sous forme de points clés, mais avec un **MAXIMUM DE 120 MOTS**. Présente chaque défi sous la forme d'une phrase concise, accompagnée d'une icône représentative (comme un emoji) au début de chaque point. Utilise un ton neutre mais constructif, en soulignant les défis d'une manière qui incite à la réflexion sans être trop critique. Assure-toi que chaque point soit clair, succinct, et directement lié aux caractéristiques clés de la personne. Voici un exemple de ce que je souhaite obtenir : exemple 1 🔄 Précipitation dans l'action : Sa tendance à agir rapidement et à prendre des risques peut parfois manquer de la réflexion nécessaire, surtout dans des situations complexes. 🌍 Interaction sociale réservée : Son indépendance et son orientation vers l'action peuvent parfois la rendre moins attentive aux besoins émotionnels des autres, ce qui pourrait créer des décalages dans les relations. 🚧 Approche directe et sans détour : Sa communication franche et directe, bien que souvent efficace, peut parfois être perçue comme un manque de tact, ce qui pourrait engendrer des malentendus. ⏩ Tolérance limitée à l'attente : Son désir de voir des résultats rapides peut rendre difficile pour elle de tolérer les délais ou les processus lents, ce qui pourrait mener à une frustration dans des environnements moins dynamiques.\n "


context_append(forces_text, defis_prompt)

defis = generateur_texte(message_data, 250)

defis_text = defis.choices[0].message.content

#Section "Perception du changement"

changement_prompt = f"""Je souhaite que tu crées une section 'Perception du changement' dans un **MAXIMUM DE 100 MOTS** qui décrit comment une personne perçoit et réagit au changement. Cette fois-ci,  en se basant sur la totalité des question du questionnaire suivant:\n {synergia_couleur_string}.\n Le texte doit être en plusieurs paragraphes, décrivant comment la personne aborde le changement, en mettant en avant son attitude générale, ses forces, et son approche face aux nouvelles situations. Inclut un paragraphe final qui la compare avec une perception opposée. Décris comment la personne voit le changement – est-ce qu'elle l'embrasse, le redoute, ou le considère comme une opportunité ? Mentionne la manière dont la personne s'adapte aux nouvelles situations. Pour la dernière partie du texte, mentionne plutôt une perception qui serait opposée à celle de la personne décrite. Par exemple, si la personne est rapide et positive, mentionne que d'autres pourraient la percevoir comme étant trop précipitée ou optimiste, tandis qu'elle pourrait percevoir ces personnes comme trop prudentes ou focalisées sur les risques. Utilise un ton engageant, tout en restant réaliste et nuancé. Assure-toi que la section finale sur la perception opposée soit constructive et présente un équilibre entre les différentes perspectives. Voici un exemple de ce que je souhaite obtenir : [exemple 1 Maxime perçoit le changement comme une opportunité excitante et un moteur de croissance personnelle et professionnelle. Son audace et son esprit d'initiative le rendent particulièrement réceptif aux nouvelles expériences et aux défis. Il aborde le changement avec un optimisme contagieux, voyant chaque nouveauté comme une chance de tester ses capacités de leader et d'innovateur. Maxime est naturellement incliné à embrasser le changement plutôt que de le redouter, considérant chaque transition comme une porte ouverte vers de nouvelles possibilités et aventures. Sa capacité à prendre des décisions rapides et à s'adapter spontanément le rend apte à naviguer efficacement dans des environnements en constante évolution. Pour Maxime, le changement est synonyme de progrès et d'opportunités pour influencer positivement son entourage et laisser une empreinte durable. À noter que certaines personnes pourraient percevoir l'attitude de Maxime comme étant trop rapide ou optimiste, ce qui pourrait leur sembler précipité ou risqué. En revanche, Maxime pourrait percevoir ces personnes comme étant trop prudentes ou trop axées sur les détails, ce qui pourrait lui sembler freiner l'innovation et l'action rapide.\n "Je souhaite que vous évaluiez la perception du changement d'une personne en fonction de deux critères :

1. Vitesse d'Adaptation : Indique si la personne s'adapte (1) plus rapidement que la moyenne, (2) dans la moyenne, ou (3) plus lentement que la moyenne face aux changements, en te basant sur ses réponses au questionnaire.

2. Niveau de Confiance : Indique si la personne est (1) plus confiante que la moyenne, (2) dans la moyenne, ou (3) moins confiante que la moyenne par rapport au changement, en analysant ses réponses.

Je ne souhaite pas un texte explicatif, juste une évaluation claire sous la forme : "Plus rapide que la moyenne", "Dans la moyenne", ou "Plus lent que la moyenne" pour la vitesse d'adaptation et la confiance." """


context_append(defis_text, changement_prompt)

changements = generateur_texte(message_data, 350)

changements_text = changements.choices[0].message.content


#Section Perception des relations interpersonnelles

interpersonnelles_prompt = """Utilise les questions 1 à 15 "Je souhaite que tu crées une section 'Perception des relations interpersonnelles' dans un MAXIMUM DE 150 MOTS qui décrit comment une personne perçoit et gère ses relations avec les membres de son équipe, en se basant sur ses réponses au questionnaire de 1 à 15 et ses caractéristiques personnelles. Le texte doit être en plusieurs paragraphes, décrivant comment la personne envisage les relations interpersonnelles, en mettant en avant son attitude générale, ses forces, et sa manière de cultiver ces relations. Inclut un paragraphe final qui compare sa perception des relations avec une perception opposée. Décris comment la personne voit et valorise ses relations – recherche-t-elle des connexions profondes, préfère-t-elle des interactions légères, ou est-elle plus réservée ? Mentionne la manière dont la personne interagit avec ses coéquipiers, en se basant sur ses réponses concernant la sociabilité, la communication, et la

gestion des conflits. Aborde aussi sa préférence pour l’harmonie ou son approche face aux tensions dans l’équipe. Pour la dernière partie du texte, mentionne une perception opposée : par exemple, si la personne évite les conflits, mentionne que d'autres pourraient la percevoir comme trop passive, tandis qu'elle pourrait percevoir ces personnes comme trop confrontationales ou impulsives. Utilise un ton engageant et nuancé, tout en restant positif."

Exemple 1 - Monsieur Test : Monsieur Test aborde les relations interpersonnelles avec une approche analytique et réfléchie. Il privilégie les relations qui apportent une certaine stabilité et qui sont fondées sur des valeurs communes, telles que la rigueur, la précision, et le respect des normes. Bien que réservé et peu sociable, il apprécie les relations qui respectent son besoin de calme et de structuration. Il n'est pas le genre à rechercher des relations superficielles ou à se précipiter dans de nouvelles interactions. Pour lui, la qualité prime sur la quantité, et il préfère s’entourer de personnes fiables et sérieuses avec qui il peut avoir des discussions profondes et enrichissantes.

Monsieur Test est également quelqu'un de prudent dans ses relations interpersonnelles. Il évite les personnes qui pourraient introduire de l'instabilité ou des comportements imprévisibles. Il préfère des interactions où l'efficacité et la logique sont au premier plan, et où les émotions sont gérées de manière rationnelle. Bien qu'il soit moins démonstratif dans ses relations, il accorde une grande importance à la loyauté et au respect mutuel.

À noter que certaines personnes pourraient percevoir l'attitude de Monsieur Test comme étant trop réservée ou rigide, ce qui pourrait leur sembler distant ou peu engageant. En revanche, Monsieur Test pourrait percevoir ces personnes comme trop spontanées ou désorganisées, ce qui pourrait lui sembler perturbant ou difficile à intégrer dans ses routines bien établies.

Exemple 2 - Madame Test : Madame Test aborde ses relations avec les membres de son équipe avec un esprit d’ouverture et d’audace. Elle privilégie les connexions légères et positives, préférant des interactions simples et sans complications. Elle ne ressent pas le besoin d’approfondir les relations, mais valorise des échanges fréquents et joyeux qui apportent une dynamique de groupe agréable. Grâce à son enthousiasme naturel, elle a tendance à attirer les autres et à maintenir une ambiance conviviale, créant ainsi un environnement propice à la collaboration et à la croissance.

Madame Test apprécie particulièrement les moments d’harmonie, où chacun se sent à l’aise et libre d’exprimer ses idées sans crainte de conflits. Bien qu’elle soit capable de gérer les tensions, elle préfère éviter les confrontations directes et favorise des solutions qui minimisent les risques de friction. Elle perçoit les relations comme des sources de plaisir, où les défis sont abordés avec légèreté.

À noter que certaines personnes pourraient percevoir Madame Test comme trop insouciante ou évitant les conflits, ce qui pourrait être perçu comme un manque de profondeur ou de sérieux dans ses relations. En contrepartie, Madame Test pourrait voir ces personnes comme trop rigides ou focalisées sur les problèmes, ce qui pourrait limiter le côté spontané et positif qu’elle cherche à maintenir dans ses relations.

" Par la suite, je souhaite obtenir deux informations basées sur les réponses aux questions 1 à 15 du questionnaire. Indique simplement :

1. Le niveau de sociabilité : est-ce que la personne est 'plus sociable que la moyenne', 'dans la moyenne' ou 'moins sociable que la moyenne' ?

2. Le niveau de confiance dans les relations : est-ce que la personne est 'plus confiante que la moyenne', 'dans la moyenne' ou 'moins confiante que la moyenne' ?"""

context_append(changements_text, interpersonnelles_prompt)

interpersonnelles = generateur_texte(message_data, 500)

interpersonnelles_text = interpersonnelles.choices[0].message.content

#Section Perception du besoin de structure et de prévisibilité

structure_prompt = """Je souhaite que tu crées une section 'Perception du besoin de structure et de prévisibilité' dans un maximum de 150 mots qui décrit comment une personne gère le besoin de structure dans ses tâches et sa préférence pour la prévisibilité dans son travail. Le texte doit être en plusieurs paragraphes, décrivant l'attitude générale de la personne face à la planification, l'organisation, et sa tolérance aux changements inattendus. Base-toi sur les réponses aux questions 1 à 15 du questionnaire. Inclut un paragraphe final qui compare sa perception avec une perception opposée. Par exemple, si la personne préfère plus de structure, mentionne que d'autres pourraient la percevoir comme trop rigide, tandis qu'elle pourrait voir ces personnes comme manquant d'organisation. Utilise un ton engageant et nuancé." [Madame Test préfère une approche flexible lorsqu'il s'agit de structurer ses tâches. Elle apprécie avoir la liberté d'organiser son travail à sa manière, sans directives strictes ou des processus rigides à suivre. Sa créativité et son esprit d'initiative lui permettent de s'adapter rapidement aux situations imprévues, et elle n'est pas dérangée par un manque de structure formelle.

En termes de prévisibilité, Madame Test est à l'aise avec les changements soudains. Elle n’a pas besoin que les projets soient planifiés à l'avance de manière rigide et accepte facilement les ajustements en cours de route. Elle prospère dans les environnements dynamiques et apprécie les défis imprévus qui stimulent sa capacité à improviser.

À noter que certaines personnes plus rigoureuses pourraient percevoir Madame Test comme manquant d'organisation ou de planification, tandis qu'elle pourrait voir ces personnes comme trop rigides ou inflexibles face aux changements.

Je souhaite obtenir deux informations basées sur les réponses aux questions 1 à 15 du questionnaire concernant :

1. Le besoin de structure dans les tâches : est-ce que la personne a un besoin de structure 'plus que la moyenne', 'dans la moyenne' ou 'moins que la moyenne' ?

2. La prévisibilité dans le travail : est-ce que la personne préfère 'plus de prévisibilité que la moyenne', 'dans la moyenne' ou 'moins de prévisibilité que la moyenne' ?"""

context_append(interpersonnelles_text, structure_prompt)

structure = generateur_texte(message_data, 500)

structure_text = structure.choices[0].message.content


#Section "Perception défis, problèmes et difficultés"

problemes_prompt = """Je souhaite que tu crées une section 'Perception des défis, problèmes et difficultés' dans un **MAXIMUM DE 150 MOTS** qui décrit comment une personne perçoit et gère les défis, les problèmes, et les difficultés, en se basant sur ses réponses du questionnaire DISC de la question précédente et ses caractéristiques personnelles. Le texte doit être en plusieurs paragraphes, décrivant l'attitude générale de la personne face aux défis, en mettant en avant son approche, ses forces, et ses éventuelles zones d'amélioration. Inclut un paragraphe final qui compare sa perception des défis avec une perception opposée. Décris comment la personne voit les défis – les perçoit-elle comme des opportunités d'apprentissage, des obstacles à surmonter, ou des situations stressantes ? Mentionne ses stratégies pour gérer les problèmes, comme l'analyse, la patience, ou la collaboration. Mentionne la manière dont la personne aborde les problèmes, en se basant sur ses réponses concernant l'impulsivité, la méthode, la tolérance au stress, et la collaboration. Aborde aussi ses préférences pour l'analyse ou l'action rapide. Pour la dernière partie du texte, au lieu de mentionner une dominance de couleur, mentionne une perception qui serait opposée à celle de la personne décrite. Par exemple, si la personne est prudente et méthodique, mentionne que d'autres pourraient la percevoir comme trop lente, tandis qu'elle pourrait percevoir ces personnes comme trop impulsives ou agressives. Utilise un ton engageant et nuancé, en restant réaliste et en soulignant les forces et les défis potentiels de la personne. Voici un exemple de ce que je souhaite obtenir : [Exemple 1 Madame Test perçoit les défis, les problèmes, et les difficultés comme des occasions de démontrer son audace, sa créativité, et sa capacité à prendre des décisions rapidement. Elle aborde ces situations avec un esprit entreprenant, préférant l'action immédiate à l'analyse prolongée. Pour elle, chaque obstacle est une chance de prouver son indépendance et de mettre en avant son esprit d'initiative. Elle n'hésite pas à se lancer dans l'inconnu, voyant dans les difficultés une opportunité d'explorer de nouvelles solutions et de repousser les limites établies.\n Son approche est marquée par une volonté de maximiser les expériences positives, même dans les moments difficiles. Madame Test préfère une stratégie proactive, cherchant à surmonter les obstacles avec détermination et en gardant un regard optimiste sur l'issue. Elle valorise les solutions innovantes et n'a pas peur de remettre en question les méthodes traditionnelles si elle pense qu'une approche différente pourrait être plus efficace.\n À noter que certaines personnes pourraient percevoir l'attitude de Madame Test comme étant trop impulsive ou risquée, ce qui pourrait leur sembler précipité ou imprudent. En revanche, Madame Test pourrait percevoir ces personnes comme étant trop prudentes ou lentes à réagir, ce qui pourrait lui sembler freiner la progression et limiter les opportunités d'innovation.\n "Je souhaite obtenir deux informations basées sur les réponses au questionnaire :

1. Positivité face aux défis : Indique si la personne est 'plus positive que la moyenne', 'dans la moyenne' ou 'moins positive que la moyenne' lorsqu'elle fait face aux défis et difficultés.

2. Gestion du stress : Indique si la personne gère le stress 'mieux que la moyenne', 'dans la moyenne' ou 'moins bien que la moyenne'."""


context_append(structure_text, problemes_prompt)

problemes = generateur_texte(message_data, 350)

problemes_text = problemes.choices[0].message.content


#Section "Encore un peu plus sur toi"

toi_prompt = f"""Je souhaite que tu crées une section 'Valeurs et motivations' qui décrit les valeurs principales et les motivations d'une personne, en se basant sur ses réponses au questionnaire DISC, ses caractéristiques personnelles, et les réponses aux questions 12 à 16 ainsi que les questions à développement de la fin. Voici le questionnaire :\n {synergia_section_motivation_string} et {synergia_section_dev_string}\n Le texte doit être en plusieurs paragraphes, ***DANS UN MAXIMUM DE 200 MOTS***, mettant en avant les aspects personnels de la personne en montrant comment ses valeurs influencent ses actions et ses décisions dans différents contextes de sa vie. Décris ce que la personne valorise dans sa vie personnelle, sa vie professionnelle, ses loisirs, et ses interactions avec ses proches. Mentionne ce qui motive la personne dans son travail – est-ce l'innovation, l'engagement, la rigueur, ou le désir d'influencer positivement son environnement ? Évoque ce qui est important pour elle. Utilise un ton inspirant et nuancé, qui met en lumière les forces et les motivations de la personne. Voici un exemple de ce que je souhaite obtenir : [Exemple 1 : Madame Test valorise avant tout la liberté et l’indépendance, que ce soit dans sa vie personnelle ou professionnelle. Elle a créé une entreprise d’animations à domicile et de consultations en entreprise, cherchant à inspirer et à influencer positivement son entourage. Son aspiration à long terme est de bâtir un réseau de franchisés qui partagent sa vision, lui permettant de rester alignée, motivée, et fière de son parcours tout en vivant une vie pleine de sens.\n Dans sa vie personnelle, Madame Test se connecte avec elle-même à travers des moments de solitude en faisant du sport, du ménage ou du plein air tout en écoutant des podcasts, ce qui nourrit son besoin de liberté. Elle apprécie également le sport d’équipe, une façon pour elle de créer des connexions intenses tout en prenant soin de son corps. Elle accorde une grande importance à ses moments de qualité avec son conjoint, où le partage et la complicité renforcent leur relation. \n Madame Test est motivée par l’innovation et l’exploration de projets excitants. Elle ne craint pas de prendre des risques et préfère l’action à l’attente, valorisant les expériences positives et l’impact qu’elle peut avoir sur les autres. Sa réussite personnelle, comme avoir pris le temps de réaligner sa vie, reflète son engagement à vivre selon ses propres termes, en étant libre et authentique.\n """



message_data.append( 
  {
    "role": "assistant", 
    "content": problemes_text
  }
)
  
message_data.append(
    {
        "role": "user",
        "content": toi_prompt
    }
)

toi = generateur_texte(message_data, 500)

toi_text = toi.choices[0].message.content


#Section "Valeurs Schwartz"

schwartz_prompt = """Je souhaite que tu identifies les trois principales motivations d'une personne selon le modèle de Schwartz, ***J'AI BESOIN DE SEULEMENT LES TROIS MOTS***, en se basant sur l'ensemble des réponses au questionnaire de la section précédente, avec une attention particulière aux questions 12 à 16 ainsi qu’aux réponses à développement. Analyse les réponses pour repérer les valeurs dominantes en utilisant les dimensions du modèle de Schwartz (ex. hédonisme, stimulation, autonomie, sécurité, etc.). Évalue quelles valeurs ressortent le plus fortement en fonction des réponses. Attribue un score à chaque dimension de Schwartz en fonction des réponses fournies, notamment celles qui reflètent des thèmes comme l'indépendance, la tradition, le plaisir, la sécurité, l'innovation, etc. Sélectionne les trois dimensions avec les scores les plus élevés pour définir les principales motivations. Présente les trois principales motivations identifiées, accompagnées d'une brève description expliquant pourquoi ces motivations sont les plus fortes chez la personne, en se basant sur les réponses spécifiques du questionnaire."""

message_data.append( 
  {
    "role": "assistant", 
    "content": toi_text
  }
)
  
message_data.append(
    {
        "role": "user",
        "content": schwartz_prompt
    }
)

schwartz = generateur_texte(message_data, 400)

schwartz_text = schwartz.choices[0].message.content


#Section Valeur et motivations

valeur_prompt = """Je souhaite que tu identifies et décrives **QUATRES MOTIVATIONS SPÉCIFIQUES** et précises pour une personne, basées sur l'ensemble de ses réponses au questionnaire, en incluant particulièrement les deux dernières questions à développement.***LE TEXTE DOIT ÊTRE D'UN MAXIMUM DE 150 MOTS***. Prends aussi en considération les couleurs de personnalité DISC de la personne. Les motivations doivent refléter ce qui pousse réellement cette personne à agir dans sa vie personnelle et professionnelle. Je veux que tu utilises des déductions et reformulations sans répéter les mots exacts de la personne. (Exemple; , Accomplissement personnel, Reconnaissance sociale,  Croissance personnelle,  Sécurité financière, Liberté d’action, Impact sur les autres,  Plaisir et divertissement, Réussite professionnelle,  Apprentissage continu,  Relations familiales,  Stabilité émotionnelle,  Avoir un objectif clair,  Compétition et défis,  Amélioration de soi,  Innovation et créativité,  Contribution à une cause,  Autonomie et indépendance,  Appartenance à un groupe, Exploration et aventure,  Spiritualité et connexion intérieure). Pour chaque motivation, développe des actions concrètes et inspirantes qui pourraient l'aider à poursuivre ses objectifs. Assure-toi que chaque motivation soit présentée de manière unique et engageante, avec des exemples pratiques et des suggestions spécifiques. Voici un exemple de format que je souhaite obtenir pour une motivation : Exemple 1\n •  Madame Test est motivée par l’innovation et la recherche de projets excitants.\n 🚀 Lancer des Initiatives Innovantes : Propose des idées nouvelles dans ton entreprise et cherche constamment à sortir des sentiers battus. Créer des franchises pour tes animations à domicile peut répondre à ton désir d’expansion et de nouveauté.\n 🧩 Participer à des Conférences sur l’Innovation : Assiste à des événements ou conférences sur les nouvelles tendances dans ton domaine, pour alimenter ta soif de projets excitants et de connaissances actuelles.\n 📝 Brainstorming Créatif : Organise des sessions de brainstorming pour développer des concepts nouveaux, que ce soit pour ton entreprise ou des projets personnels. Cela alimente ton esprit d’innovation tout en explorant des terrains inconnus.\n 🎯 Collaborations avec des Esprits Créatifs : Associe-toi à des personnes ou des équipes qui partagent ta passion pour l’innovation. Les échanges d’idées peuvent inspirer et revitaliser tes projets.\n """




message_data.append( 
  {
    "role": "assistant", 
    "content": schwartz_text
  }
)
  
message_data.append(
    {
        "role": "user",
        "content": valeur_prompt
    }
)

valeur = generateur_texte(message_data, 500)

valeur_text = valeur.choices[0].message.content



#section Toi et le marché du travail

travail_prompt = """Je souhaite que tu rédiges un texte complet qui décrit le profil professionnel d’une personne, en utilisant ses réponses au questionnaire, ses traits de personnalité DISC, et ses motivations principales. Le texte doit suivre une structure précise et inclure plusieurs paragraphes décrivant différents aspects de sa personnalité et de sa façon de travailler, ***DANS UN MAXIMUM DE 325 MOTS***. Assure-toi d’utiliser un langage fluide, engageant, et de ne pas répéter les mêmes mots ou expressions. Voici la structure à suivre :\n1.	Introduction de la Personne :\nDébute par une description de la nature et des traits de personnalité principaux de la personne, et comment ces caractéristiques influencent sa manière de travailler. Mets en avant ce qui la rend unique dans son approche professionnelle.\n2.	Compétences et Style de Travail :\nPrésente les compétences professionnelles distinctives de la personne et son style de travail. Décris comment ses traits se manifestent concrètement dans son travail, en expliquant ce qui la rend efficace dans son rôle. Inclue des exemples ou scénarios pour illustrer ces compétences.\n3.	Approche en Équipe et Prise de Décision :\nDécris comment la personne contribue à la dynamique d’équipe et à la prise de décision. Mentionne sa manière de collaborer, son style de communication, et comment elle aborde les défis en groupe. Ajoute un aperçu de la gestion des conflits ou des situations délicates pour montrer comment elle réagit en moments critiques.\n4.	Style de Leadership :\nSi la personne est en position de leadership, décris son style de gestion et comment elle est perçue par les autres. Mets en avant ses qualités de leader et la façon dont elle inspire, motive, ou guide son équipe. \n5.	Impact sur l’Équipe :\nConclus en expliquant l’impact de la personne sur ses collègues et sur la dynamique de l’équipe. Mentionne comment elle influence son entourage, crée une dynamique de travail spécifique, et en quoi ses qualités apportent de la valeur. \nAssure-toi que le texte soit équilibré, nuancé, et qu’il donne une vision complète de la personne en montrant à la fois ses forces et ses zones d’amélioration. Il ne doit pas répéter les mêmes caractéristiques fréquemment. Inclue des exemples concrets et explore les aspects relationnels pour offrir un portrait riche et engageant. Voici un exemple de ce que je souhaite obtenir : [Exemple 1 :Madame Test se distingue par sa nature audacieuse et indépendante, qui transparaît dans sa manière de travailler. Elle valorise la liberté d’action et l’autonomie, ce qui lui permet de prendre des initiatives audacieuses et d’aborder les projets avec une grande créativité. Son désir de se démarquer et de créer un impact positif est évident dans chaque aspect de son travail. Son approche professionnelle est marquée par une volonté constante de repousser les limites, tant pour elle-même que pour son équipe.\nSur le plan professionnel, Madame Test se révèle particulièrement efficace dans des contextes où l’innovation est encouragée. Elle excelle à transformer des idées novatrices en actions concrètes, notamment lors de la création d’animations à domicile ou dans des projets qui demandent une touche personnelle. Son style de travail est dynamique et énergique : elle aime explorer de nouvelles voies et se lance sans hésiter dans des initiatives non conventionnelles. Par exemple, lorsqu'elle initie un projet, elle s’assure que chaque détail reflète son sens de l’originalité et de la nouveauté, apportant ainsi une dimension unique à ses réalisations.\nDans une équipe, Madame Test adopte une approche directe et proactive, contribuant à la prise de décision avec assurance. Elle n’hésite pas à exprimer ses idées et à encourager les autres à sortir de leur zone de confort. Sa capacité à gérer des situations délicates avec un mélange d’audace et de réflexion rapide lui permet de naviguer efficacement dans les moments critiques. Elle sait mobiliser son équipe en utilisant son enthousiasme contagieux, même si son style peut parfois dérouter ceux qui préfèrent une approche plus structurée et méthodique.\nEn tant que leader, Madame Test inspire par sa détermination et son esprit d’initiative. Elle est perçue comme une figure motivante, toujours prête à explorer de nouvelles stratégies et à encourager son équipe à faire de même. Sa capacité à diriger avec confiance tout en laissant de la place à l’innovation en fait une leader qui se démarque par son approche visionnaire. Elle sait guider son équipe avec un équilibre entre indépendance et engagement, créant un environnement où chacun se sent libre de contribuer.\nL’impact de Madame Test sur son entourage est marqué par sa capacité à insuffler une dynamique positive et stimulante. Elle influence ses collègues par son énergie et sa passion pour l’innovation, poussant l’équipe à se dépasser et à embrasser le changement avec enthousiasme. Ses qualités font d’elle une alliée précieuse, capable de transformer la dynamique de travail en un espace où les idées audacieuses et les approches non conventionnelles sont non seulement acceptées, mais encouragées.\n."""


message_data.append( 
  {
    "role": "assistant", 
    "content": valeur_text
  }
)
  
message_data.append(
    {
        "role": "user",
        "content": travail_prompt
    }
)

travail = generateur_texte(message_data, 750)

travail_text = travail.choices[0].message.content

#Section Environnements de travail favorable

environnement_prompt = """Je souhaite que tu rédiges un texte complet qui décrit l'environnement de travail favorable pour une personne, en se basant sur ses réponses au questionnaire, ses traits de personnalité DISC, et ses motivations principales, ***DANS UN MAXIMUM DE 300 MOTS***. Ne prends pas en compte les réponses aux questions à développement. Le texte doit suivre une structure précise, incluant plusieurs paragraphes qui décrivent les conditions de travail optimales pour cette personne, ainsi que les environnements les moins favorables et les raisons pour lesquelles ils sont moins adaptés. Assure-toi de développer pourquoi certains environnements sont positifs pour la personne et pourquoi d'autres ne le sont pas. Intègre également une section qui décrit ses préférences en matière de contacts sociaux, en précisant si ces interactions lui donnent de l’énergie ou la drainent, afin de refléter son niveau d’extraversion ou d’intraversion. Utilise un langage fluide, engageant, et évite de répéter les mêmes mots ou expressions. Voici la structure à suivre :\n1.	Introduction :\nDébute en expliquant dans quel type d'environnement la personne s’épanouit le mieux. Mentionne les caractéristiques principales de l’environnement qui lui permettent de se sentir à l’aise et de performer, en lien avec ses traits de personnalité.\n2.	Culture d'entreprise et style de travail :\nDécris les éléments de la culture d’entreprise qui sont les plus compatibles avec la personne, comme l'innovation, la prise de risque, ou la collaboration. Précise ce qui lui permet d'exprimer ses forces et de s’engager pleinement dans son travail, en élaborant sur les raisons pour lesquelles ces éléments sont positifs pour elle.\n3.	Préférences en Matière de Contacts Sociaux :\nMentionne si la personne préfère des interactions sociales fréquentes ou si elle privilégie des échanges plus authentiques et de qualité. Précise si ces interactions lui donnent de l’énergie ou la drainent, afin de déterminer son niveau d’extraversion ou d’intraversion. Explique comment ces préférences influencent son environnement de travail idéal.\n4.	Rôle et contribution :\nExplique comment la personne se comporte dans cet environnement et comment elle utilise ses compétences pour apporter de la valeur. Mentionne sa façon de contribuer à l’équipe ou au projet, et comment l’environnement lui permet de mettre en avant son leadership ou ses capacités spécifiques.\n5.	Environnements Moins Favorables :\nAjoute une section sur les types d’environnements qui conviennent le moins à la personne. Explique pourquoi ces environnements sont moins favorables, en lien avec ses traits de personnalité et ses préférences, et comment cela peut affecter sa performance ou son bien-être. Développe sur les aspects spécifiques qui rendent ces environnements difficiles pour elle.\n6.	Conclusion :\nConclus en résumant ce qui rend cet environnement idéal pour la personne, en soulignant comment cela maximise son potentiel et son épanouissement professionnel, tout en notant l'importance d'éviter les environnements moins adaptés.\nAssure-toi que le texte reflète fidèlement la personnalité et les préférences de la personne, en montrant clairement comment un environnement de travail spécifique peut l’aider à s’épanouir, et pourquoi d'autres environnements pourraient nuire à sa performance. Utilise des phrases positives et engageantes pour créer un portrait motivant et précis de son environnement de travail idéal et moins idéal. Voici un exemple de ce que je souhaite obtenir : \n: [Exemple 1 Monsieur Test s’épanouit dans un environnement de travail structuré et méthodique, où l’organisation, la stabilité et les normes élevées sont valorisées. Il excelle dans des contextes où les processus clairs et les règles définies permettent une gestion précise et ordonnée des projets. Ces environnements lui offrent un cadre sécurisant, lui permettant de se concentrer sur l’atteinte de l’excellence et la production de résultats de haute qualité. Le respect des procédures et la cohérence dans les pratiques lui permettent de minimiser les risques et de garantir un travail impeccable, aligné avec ses standards élevés.\nMonsieur Test apprécie particulièrement les cultures d'entreprise qui valorisent la planification, la précision, et le respect des protocoles établis. Ces contextes sont positifs pour lui car ils répondent à son besoin de clarté et de rigueur, lui offrant la stabilité nécessaire pour performer à son meilleur. La structure et l'organisation de ces environnements lui permettent de canaliser son souci du détail et sa capacité à analyser les données de manière approfondie, contribuant ainsi de manière efficace à l'atteinte des objectifs communs.\nEn matière de contacts sociaux, Monsieur Test préfère des interactions qui sont ciblées et pertinentes, plutôt que des échanges sociaux fréquents ou superficiels. Les contacts constants et les interactions trop nombreuses peuvent le drainer, affectant sa concentration et son efficacité. Il se sent plus énergisé lorsqu'il peut travailler de manière autonome ou dans des environnements où les échanges sont constructifs et limités à ce qui est nécessaire pour avancer dans les projets. Cela reflète une tendance plus introvertie, où les échanges de qualité priment sur la quantité.\nEn revanche, Monsieur Test est moins à l’aise dans des environnements trop dynamiques, imprévisibles, ou désorganisés, où les règles sont floues et les structures peu respectées. Les cultures d’entreprise qui favorisent l’improvisation, le changement constant, ou une approche trop flexible peuvent créer du stress et réduire son efficacité. Ces environnements peuvent affecter son bien-être car ils manquent de la clarté et de la stabilité dont il a besoin pour se sentir en contrôle et motivé.\nEn résumé, Monsieur Test s’épanouit dans des environnements de travail ordonnés et bien structurés, où ses compétences méthodiques et analytiques peuvent briller. Les environnements trop chaotiques ou axés sur l’improvisation risquent de nuire à son engagement et à sa performance, limitant ainsi sa capacité à apporter une contribution optimale à son équipe et à son organisation.\n"""



message_data.append( 
  {
    "role": "assistant", 
    "content": travail_text
  }
)
  
message_data.append(
    {
        "role": "user",
        "content": environnement_prompt
    }
)

environnement = generateur_texte(message_data, 650)

environnement_text = environnement.choices[0].message.content



#Section Exemples d’environnements de travail favorables

ex_env_prompt = """Je souhaite que tu rédiges une section qui présente des environnements de travail favorables pour une personne, en se basant sur l'entièreté de ses réponses au questionnaire et ses traits de personnalité DISC, ***DANS UN MAXIMUM DE 200 MOTS***. Propose des suggestions qui sont en lien avec ce qu'elle fait actuellement, mais inclut également des suggestions d'environnements qui pourraient lui convenir parfaitement selon ses réponses. Utilise un ton positif et engageant, et présente chaque suggestion de manière claire avec une phrase d'introduction suivie d'une explication précise du pourquoi cet environnement est favorable à la personne. Utilise des icônes pertinentes pour chaque suggestion pour rendre le texte plus visuel et attrayant. Voici la structure à suivre :\n1.	Présente l'environnement avec un titre et une icône :\nDonne un titre à chaque environnement de travail proposé avec une icône pertinente, comme : “Administration et Support Organisationnel 🏢”.\n2.	Décris pourquoi cet environnement convient :\nPour chaque suggestion, explique brièvement pourquoi cet environnement est favorable à la personne, en reliant cette explication à ses compétences, traits de personnalité, et préférences indiquées dans le questionnaire.\n3.	Inclut des exemples concrets ou des tâches typiques :\nMentionne des tâches spécifiques ou des aspects de l’environnement qui exploitent les forces et les compétences de la personne.\n4.	Assure-toi d’inclure des suggestions variées :\nInclut à la fois des environnements en lien avec ce qu’elle fait actuellement et d’autres qui pourraient être de bonnes options selon ses réponses, même si elles ne sont pas directement liées à son parcours actuel.\nAssure-toi que le texte soit concis, clair, et montre des possibilités de carrière ou d’environnements de travail dans lesquels la personne pourrait s’épanouir et utiliser ses forces au maximum. Voici un exemple de ce que je souhaite obtenir : [Exemple 1 : Entrepreneuriat et Création de Projets Innovants 🚀\nMadame Test excelle dans des environnements où l’innovation, l’indépendance, et la prise de risque sont au cœur des activités. En tant qu'entrepreneure, elle peut exploiter sa créativité et sa passion pour les nouvelles idées, tout en jouissant d'une grande liberté d’action. Ce cadre lui permet de prendre des décisions audacieuses et de mener des projets qui sortent des sentiers battus, alignés avec son besoin de liberté et d'autonomie.\nConsultation et Coaching en Développement Personnel 🧠\nAvec sa capacité à motiver et à influencer positivement les autres, Madame Test serait idéale pour des rôles en consultation ou en coaching. Ces environnements favorisent la communication directe, l'impact positif, et l’innovation, répondant parfaitement à son désir de faire une différence tout en travaillant de manière indépendante. Son enthousiasme et son approche inspirante peuvent transformer les expériences des personnes qu’elle accompagne.\nÉvénementiel et Organisation d’Animations à Domicile 🎉\nMadame Test se sentirait à l’aise dans des rôles qui impliquent la création d'événements et l'animation, où elle peut maximiser les expériences positives pour les participants. Son esprit innovateur et son désir de sortir des conventions s’alignent avec des activités dynamiques et créatives qui lui permettent de partager ses idées tout en interagissant avec les autres dans des contextes stimulants et sociaux.\nMarketing Créatif et Publicité 📣\nSon goût pour l'originalité et sa capacité à penser hors des sentiers battus rendent Madame Test particulièrement adaptée aux environnements de marketing créatif et de publicité. Elle peut y exploiter son sens de l’innovation, son esprit d’indépendance, et sa volonté de prendre des risques calculés pour créer des campagnes qui se démarquent et captent l’attention du public.\nRôle de Leadership dans Startups ou PME 💡\nMadame Test pourrait également exceller dans des rôles de leadership au sein de startups ou de PME, où la flexibilité et l'innovation sont valorisées. Ces environnements lui permettent de diriger des équipes avec audace et de mettre en place des stratégies novatrices tout en influençant directement la direction de l'entreprise. Sa capacité à inspirer et à motiver les autres serait un atout majeur dans ce type de contexte.\n"""



message_data.append( 
  {
    "role": "assistant", 
    "content": environnement_text
  }
)
  
message_data.append(
    {
        "role": "user",
        "content": ex_env_prompt
    }
)

ex_env = generateur_texte(message_data, 350)

ex_env_text = ex_env.choices[0].message.content

#Section Tes couleurs en couple

couple_prompt = f"""Je souhaite que tu rédiges un texte ***D'UN MAXIMUM DE 200 MOTS*** qui décrit le profil de la personne dans sa relation de couple, en utilisant spécifiquement ces réponses :\n {synergia_section_couple_string}\n Pour chaque couleur (rouge, jaune, vert, bleu), mets en avant les points forts basés sur les réponses spécifiques données aux questions de cette section et mentionne aussi les aspects moins présents ou absents pour chaque couleur. Je veux que tu accordes à chaque énoncé une couleur pour t'aider à calculer le résultat, et que tu donnes un % calculé en fonction de donner une pondération à chaque énoncé. N’utilise pas de pourcentages mais qualifie les scores comme "fort", "modéré" ou "faible" selon les réponses. Voici comment structurer le texte :\n1.	Jaune (Influence) : Décris les forces telles que la convivialité, la sociabilité, et l'engagement émotionnel si le score est élevé. Si la couleur est moins présente, mentionne le manque de dynamisme social ou d'influence, indiquant une préférence pour d'autres types d'interactions.\n2.	Rouge (Dominance) : Mets en avant la prise d'initiative et la proactivité si le score est fort, expliquant comment la personne prend les devants dans la relation. Si le score est faible, note l'absence de traits dominants ou assertifs, avec une tendance à privilégier les décisions partagées ou la collaboration plutôt que le contrôle.\n3.	Vert (Stabilité) : Décris les points forts liés à la stabilité émotionnelle, à l'écoute et à la création d’un environnement serein si le score est élevé. Si cette couleur est moins présente, mentionne une tendance à moins rechercher l’harmonie ou la stabilité émotionnelle.\n4.	Bleu (Conformité) : Souligne les forces analytiques et la précision dans la communication si le score est élevé, en mettant en avant l'importance de la clarté et de la réflexion dans les échanges. Si le score est faible, note l’absence de structure ou de rigueur dans la communication, avec une préférence pour des approches moins formelles.\nAssure-toi que le texte soit équilibré, nuancé, et donne une vision complète de la dynamique de la personne en couple. Utilise un langage engageant et précis, en montrant à la fois ce qui est présent et ce qui manque dans chaque trait DISC."\n(Exemple 1 : Jaune (Influence) : Modéré\nMadame Test montre une influence modérée en matière de convivialité et d’engagement social dans sa relation de couple. Elle privilégie les discussions dynamiques et communicatives, mettant l’accent sur la clarté et l’échange. Cependant, ses interactions ne sont pas toujours axées sur la spontanéité ou l’exubérance sociale, ce qui montre qu’elle préfère des moments de connexion réfléchis et ciblés plutôt que des échanges trop fréquents ou légers.\nRouge (Dominance) : Fort\nMadame Test affiche un score fort en rouge, ce qui se traduit par une prise d’initiative marquée et une volonté de s’exprimer clairement dans la relation. Elle n’hésite pas à communiquer ses attentes de manière directe et à prendre des décisions rapidement lorsqu’il le faut. Cette approche proactive montre son désir de mener et d’influencer activement les dynamiques de son couple, tout en restant ouverte à la collaboration.\nVert (Stabilité) : Modéré\nSon score modéré en vert indique une appréciation pour l’harmonie et la stabilité émotionnelle, mais ce n’est pas sa priorité principale. Madame Test veille à maintenir un environnement relativement calme et serein, mais elle n’est pas exclusivement focalisée sur le maintien constant de l’harmonie. Elle est capable d’écouter et de soutenir son partenaire, mais sans nécessairement éviter les confrontations si elles s’avèrent nécessaires pour avancer.\nBleu (Conformité) : Fort\nMadame Test montre une forte affinité pour la réflexion et l’analyse dans ses interactions. Elle s’assure que ses attentes sont bien comprises en les expliquant en détail, ce qui souligne son besoin de précision et de clarté dans la communication. Cependant, elle n’adopte pas toujours une approche structurée ou formelle, indiquant une préférence pour une certaine flexibilité tout en gardant un œil sur les détails importants.\n"""



message_data.append( 
  {
    "role": "assistant", 
    "content": ex_env_text
  }
)
  
message_data.append(
    {
        "role": "user",
        "content": couple_prompt
    }
)

couple = generateur_texte(message_data, 500)

couple_text = couple.choices[0].message.content



#Section Portrait

portrait_prompt = """Je souhaite que tu rédiges un texte ***D'UN MAXIMUM DE 200 MOTS*** qui décrit le profil de la personne dans sa relation de couple, en utilisant uniquement les informations de la section couple du questionnaire DISC de la section précédente. On ne sait pas si la personne à un ou une partenaire alors on va faire un texte inclusif. Le texte doit détailler les forces de la personne en tant que partenaire, en mettant en avant son style de communication, son approche au soutien émotionnel, et la manière dont elle aborde les objectifs communs et les projets futurs. Voici les éléments à inclure :\n1.	Introduction sur la Personne : Débute par une description des principaux traits de personnalité en couple, tels que la préférence pour la structure, la stabilité ou la spontanéité, selon les réponses.\n2.	Style de Communication : Explique comment la personne communique ses attentes et assure une compréhension claire entre les partenaires. Mentionne si elle privilégie une communication détaillée, directe ou émotionnelle.\n3.	Approche au Soutien Émotionnel : Décris la manière dont la personne offre du soutien à son partenaire, en mettant en avant son écoute, ses conseils réfléchis, ou ses solutions pratiques.\n4.	Stabilité Émotionnelle et Harmonie : Mentionne l'importance qu'elle accorde à la stabilité émotionnelle et à la sérénité dans la relation, et comment cela contribue à un environnement paisible.\n5.	Objectifs Communs et Personnels : Parle de l'importance des objectifs partagés et de la manière dont la personne s'engage à les atteindre en collaboration avec son partenaire.\n6.	Joie et Spontanéité : Décris comment la personne apporte de la joie et de la légèreté au quotidien, et en quoi son style unique rend chaque journée spéciale.\n7.	Approche des Projets Futurs : Explique comment la personne aborde les discussions sur les projets futurs, si elle préfère planifier, discuter spontanément ou réfléchir calmement aux décisions importantes.\nAssure-toi que le texte soit fluide, nuancé, et qu'il donne une vision complète de la personne en couple, en combinant organisation, soutien émotionnel et joie de vivre." \n(exemple1 :  Monsieur Test est un partenaire qui valorise l’harmonie, l’écoute et une approche réfléchie dans sa relation de couple. En tant que pacificateur, il veille à maintenir un environnement serein, évitant les conflits et favorisant une communication calme et posée. Sa manière de communiquer est détaillée et réfléchie, préférant expliquer ses attentes clairement pour éviter tout malentendu. Cette approche structurée aide à renforcer la compréhension mutuelle et à créer un climat de confiance dans la relation.\nMonsieur Test est également un soutien précieux pour son partenaire. Il écoute avec attention et apporte des conseils réfléchis, montrant un engagement profond envers le bien-être de l’autre. Sa capacité à maintenir la stabilité émotionnelle est un atout majeur dans son couple, car il crée un espace où chacun peut s’exprimer librement tout en se sentant soutenu. Cette attention aux besoins émotionnels permet de construire une relation fondée sur le respect mutuel et la compréhension.\nIl accorde une grande importance aux expériences partagées, apportant une énergie positive et une volonté de créer des moments agréables. Monsieur Test privilégie les discussions ouvertes et spontanées sur les projets futurs, tout en prenant le temps de réfléchir calmement aux décisions importantes. Sa capacité à maintenir l’équilibre entre réflexion et spontanéité permet de naviguer sereinement à travers les décisions communes.\nBien qu’il préfère les discussions posées, Monsieur Test ne fuit pas les confrontations lorsqu’elles sont nécessaires. Il aborde les défis avec une approche analytique, cherchant toujours à comprendre les situations avant d’agir. En résumé, Monsieur Test est un partenaire attentionné et réfléchi, qui combine harmonie, soutien émotionnel et une approche équilibrée dans sa vie de couple.\n"""



message_data.append( 
  {
    "role": "assistant", 
    "content": couple_text
  }
)
  
message_data.append(
    {
        "role": "user",
        "content": portrait_prompt
    }
)

portrait = generateur_texte(message_data, 500)

portrait_text = portrait.choices[0].message.content

#Print la totalité des textes

full_text= f"COULEURS\nbleu : {bleu}%, rouge : {rouge}%, jaune : {jaune}%, vert : {vert}%\n" + f"ARCHÉTYPE\nexploreur : {explorateur}%, protecteur : {protecteur}%, bouffon : {bouffon}%, souverain : {souverain}%\nmagicien : {magicien}%, créateur : {createur}%, héro : {hero}, citoyen : {citoyen}%\nsage : {sage}%, amant : {amant}, rebelle : {rebelle}%, optimiste : {optimiste}\n\n" + "EN BREF\n" + bref_text + "\n\n" + "Tes forces mises en lumière\n" + forces_text + "\n\n" + "Tes défis Potentiels\n" + defis_text + "\n\n" + "Perception du changement\n" + changements_text + "\n\n" + "Perception des relations interpersonnelles\n" + interpersonnelles_text + "\n\n" + "Perception dubesoin de structure et de prévisibilité\n" + structure_text + "\n\n" + "Perception des défis, problèmes et difficultés\n" + problemes_text + "\n\n" + "Encore un peu plus sur toi\n" + toi_text + "\n\n" + "Valeurs Schwartz\n" + schwartz_text + "\n\n" + "Valeur et motivation\n" + valeur_text + "\n\n" + "Toi et le marché du travail\n" + travail_text + "\n\n" + "Environnement de travail favorable\n" + environnement_text + "\n\n" + "Exemples d’environnements de travail favorables\n" + ex_env_text + "\n\n" + "Tes couleurs en couple\n" + couple_text + "\n\n" + "Ton portrait\n" + portrait_text



#POUR GÉNÉRATION DES DOSSIERS ET WORD
    
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

nom_organisateur = synergia_nom.iloc[0, 4]

nouveau_dossier = f"C:/Users/Guillaume Cloutier/OneDrive/Synergia/{nom_organisateur}/{nom}"

if not os.path.exists(nouveau_dossier):
    os.makedirs(nouveau_dossier)

# Générer le fichier Word
generate_simple_word(f"{nouveau_dossier}/{nom}", full_text)
    

