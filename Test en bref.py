import os
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
from openai import OpenAI
from openai.types import Completion, CompletionChoice, CompletionUsage
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import textwrap



  
# *****À FAIRE**** code pour automatisation, activation lors de réception d'un nouveau formulaire 

#NOM

nom = "Sébastien, Lizotte"

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

#Section "Tes défis Potentiels"

defis_prompt = "Je souhaite que tu identifies et présentes les 4 défis potentiels de cette personne basé sur son questionnaire, sous forme de points clés, mais avec un **MAXIMUM DE 120 MOTS**. Présente chaque défi sous la forme d'une phrase concise, accompagnée d'une icône représentative (comme un emoji) au début de chaque point. Utilise un ton neutre mais constructif, en soulignant les défis d'une manière qui incite à la réflexion sans être trop critique. Assure-toi que chaque point soit clair, succinct, et directement lié aux caractéristiques clés de la personne. Voici un exemple de ce que je souhaite obtenir : exemple 1 🔄 Précipitation dans l'action : Sa tendance à agir rapidement et à prendre des risques peut parfois manquer de la réflexion nécessaire, surtout dans des situations complexes. 🌍 Interaction sociale réservée : Son indépendance et son orientation vers l'action peuvent parfois la rendre moins attentive aux besoins émotionnels des autres, ce qui pourrait créer des décalages dans les relations. 🚧 Approche directe et sans détour : Sa communication franche et directe, bien que souvent efficace, peut parfois être perçue comme un manque de tact, ce qui pourrait engendrer des malentendus. ⏩ Tolérance limitée à l'attente : Son désir de voir des résultats rapides peut rendre difficile pour elle de tolérer les délais ou les processus lents, ce qui pourrait mener à une frustration dans des environnements moins dynamiques./n Exemple 2 🔄 Tendance à l'analyse excessive : Son besoin de tout analyser en détail peut parfois ralentir la prise de décision, surtout dans des situations où une action rapide est nécessaire. 🚧 Réservé dans les interactions sociales : Sa nature introvertie et son manque d'enthousiasme pour les interactions sociales peuvent le rendre distant, ce qui pourrait limiter sa capacité à créer des connexions avec les autres. 🔍 Rigidité dans l'organisation : Son attachement à l'ordre et à la méthodologie peut le rendre moins flexible face aux changements ou aux idées nouvelles, ce qui pourrait créer des tensions dans des environnements plus dynamiques. ⏳ Prise de décision prudente : Sa préférence pour la prudence et la réflexion approfondie peut parfois être perçue comme de l'hésitation, surtout dans des situations où une action plus décisive est attendue. ]. Assure-toi que les défis potentiels identifiés reflètent une vision équilibrée et réaliste de la personnalité de la personne, tout en étant présentés de manière constructive."

message_data.append( 
  {
    "role": "assistant", 
    "content": forces_text
  }
)
  
message_data.append(
    {
        "role": "user",
        "content": defis_prompt
    }
)

defis = generateur_texte(message_data, 250)

defis_text = defis.choices[0].message.content

#Section "Perception du changement"

changement_prompt = f"""Je souhaite que tu crées une section 'Perception du changement' dans un **MAXIMUM DE 200 MOTS** qui décrit comment une personne perçoit et réagit au changement. Cette fois-ci,  en se basant sur la totalité des question du questionnaire suivant:/n {synergia_section2_string}./n Le texte doit être en plusieurs paragraphes, décrivant comment la personne aborde le changement, en mettant en avant son attitude générale, ses forces, et son approche face aux nouvelles situations. Inclut un paragraphe final qui la compare avec une perception opposée. Décris comment la personne voit le changement – est-ce qu'elle l'embrasse, le redoute, ou le considère comme une opportunité ? Mentionne la manière dont la personne s'adapte aux nouvelles situations. Pour la dernière partie du texte, mentionne plutôt une perception qui serait opposée à celle de la personne décrite. Par exemple, si la personne est rapide et positive, mentionne que d'autres pourraient la percevoir comme étant trop précipitée ou optimiste, tandis qu'elle pourrait percevoir ces personnes comme trop prudentes ou focalisées sur les risques. Utilise un ton engageant, tout en restant réaliste et nuancé. Assure-toi que la section finale sur la perception opposée soit constructive et présente un équilibre entre les différentes perspectives. Voici un exemple de ce que je souhaite obtenir : [exemple 1 Maxime perçoit le changement comme une opportunité excitante et un moteur de croissance personnelle et professionnelle. Son audace et son esprit d'initiative le rendent particulièrement réceptif aux nouvelles expériences et aux défis. Il aborde le changement avec un optimisme contagieux, voyant chaque nouveauté comme une chance de tester ses capacités de leader et d'innovateur. Maxime est naturellement incliné à embrasser le changement plutôt que de le redouter, considérant chaque transition comme une porte ouverte vers de nouvelles possibilités et aventures. Sa capacité à prendre des décisions rapides et à s'adapter spontanément le rend apte à naviguer efficacement dans des environnements en constante évolution. Pour Maxime, le changement est synonyme de progrès et d'opportunités pour influencer positivement son entourage et laisser une empreinte durable. À noter que certaines personnes pourraient percevoir l'attitude de Maxime comme étant trop rapide ou optimiste, ce qui pourrait leur sembler précipité ou risqué. En revanche, Maxime pourrait percevoir ces personnes comme étant trop prudentes ou trop axées sur les détails, ce qui pourrait lui sembler freiner l'innovation et l'action rapide./n Exemple 2 : Monsieur Test perçoit le changement avec une approche méthodique et prudente. Bien qu'il soit rigoureux et axé sur l'organisation, il n'est pas immédiatement enthousiaste face aux transitions soudaines ou non planifiées. Pour lui, le changement est avant tout une occasion de mettre à l'épreuve sa capacité à maintenir un haut niveau de précision et d'exactitude. Son besoin de sécurité et son attachement aux règles établies le poussent à aborder le changement avec une certaine réserve, préférant s'assurer que chaque étape soit soigneusement planifiée et analysée avant de l'adopter./n Toutefois, Monsieur Test valorise la liberté et l'indépendance, ce qui lui permet de s'adapter lorsque le changement est nécessaire pour atteindre ses objectifs personnels ou professionnels. Il est motivé par le désir de perfectionner constamment ses compétences, ce qui le rend ouvert à des ajustements, à condition qu'ils soient bien réfléchis et qu'ils respectent ses standards élevés. Bien qu'il privilégie une approche réfléchie, il n'est pas réfractaire aux idées nouvelles, surtout si elles sont soutenues par des données concrètes et une logique solide./n À noter que certaines personnes pourraient percevoir l'attitude réfléchie de Monsieur Test comme étant trop prudente ou lente à agir, ce qui pourrait leur sembler restrictif ou trop rigide. En revanche, Monsieur Test pourrait percevoir ces personnes comme étant trop impulsives ou désorganisées, ce qui pourrait lui sembler compromettre la qualité et la fiabilité des résultats.]"""

message_data.append( 
  {
    "role": "assistant", 
    "content": defis_text
  }
)
  
message_data.append(
    {
        "role": "user",
        "content": changement_prompt
    }
)

changements = generateur_texte(message_data, 350)

changements_text = changements.choices[0].message.content


#Section "Perception des relations amicales"

amicale_prompt = """Je souhaite que tu crées une section 'Perception des relations amicales' dans un **MAXIMUM DE 200 MOTS** qui décrit comment une personne perçoit et gère ses amitiés, en se basant sur ses réponses au questionnaire de 1 à 20 comme la question précédente et ses caractéristiques personnelles. Le texte doit être en plusieurs paragraphes, décrivant comment la personne envisage les relations amicales, en mettant en avant son attitude générale, ses forces, et sa manière de cultiver ses amitiés. Inclut un paragraphe final qui compare sa perception des relations amicales avec une perception opposée. Décris comment la personne voit et valorise ses relations amicales – est-ce qu'elle recherche des connexions profondes, préfère-t-elle des interactions légères, ou est-elle réservée dans ses relations ? Mentionne la manière dont la personne interagit avec ses amis, en se basant sur ses réponses concernant la sociabilité, la communication, et la tolérance. Aborde aussi sa préférence pour l'harmonie ou son approche des conflits. Pour la dernière partie du texte, au lieu de mentionner une dominance de couleur, mentionne une perception qui serait opposée à celle de la personne décrite. Par exemple, si la personne est prudente et évite les conflits, mentionne que d'autres pourraient la percevoir comme trop passive, tandis qu'elle pourrait percevoir ces personnes comme trop confrontationales ou impulsives. Utilise un ton engageant et positif, en restant réaliste et nuancé. Voici un exemple de ce que je souhaite obtenir : [Exemple 1 Monsieur Test aborde les relations amicales avec une approche analytique et réfléchie. Il privilégie les amitiés qui apportent une certaine stabilité et qui sont fondées sur des valeurs communes, telles que la rigueur, la précision, et le respect des normes. Bien que réservé et peu sociable, il apprécie les amitiés qui respectent son besoin de calme et de structuration. Il n'est pas le genre à rechercher des relations superficielles ou à se précipiter dans de nouvelles amitiés. Pour lui, la qualité prime sur la quantité, et il préfère s'entourer de personnes fiables et sérieuses avec qui il peut avoir des discussions profondes et enrichissantes./n Monsieur Test est également quelqu'un de prudent dans ses relations amicales. Il évite les amitiés qui pourraient introduire de l'instabilité ou des comportements imprévisibles. Il préfère des interactions où l'efficacité et la logique sont au premier plan, et où les émotions sont gérées de manière rationnelle. Bien qu'il soit moins démonstratif dans ses relations, il accorde une grande importance à la loyauté et au respect mutuel./n À noter que certaines personnes pourraient percevoir l'attitude de Monsieur Test comme étant trop réservée ou rigide, ce qui pourrait leur sembler distant ou peu engageant. En revanche, Monsieur Test pourrait percevoir ces personnes comme trop spontanées ou désorganisées, ce qui pourrait lui sembler perturbant ou difficile à intégrer dans ses routines bien établies./n Exemple 2 Madame Test perçoit les relations amicales comme des espaces d'exploration, de plaisir et d'indépendance. Elle valorise les amitiés qui lui permettent de maximiser les expériences positives et d'explorer de nouvelles idées, tout en préservant sa liberté personnelle. Pour elle, les amitiés sont des opportunités de partager des moments excitants et de créer des souvenirs mémorables, souvent en dehors des conventions traditionnelles. Elle préfère les relations qui ne la contraignent pas, mais qui au contraire, encouragent sa spontanéité et son désir de nouveauté./n Son approche directe et audacieuse dans ses relations peut la rendre moins attentive aux aspects émotionnels plus subtils, préférant une communication franche et sans détour. Elle aime être entourée de personnes qui partagent son énergie et son enthousiasme pour les projets stimulants. Cependant, elle peut parfois avoir du mal à se connecter avec des amis qui recherchent davantage de stabilité ou qui sont plus attachés aux traditions et aux règles établies./n À noter que certaines personnes pourraient percevoir l'attitude de Madame Test comme étant trop indépendante ou imprévisible, ce qui pourrait leur sembler déstabilisant ou difficile à suivre. En revanche, Madame Test pourrait percevoir ces personnes comme trop attachées aux normes ou trop réticentes à sortir de leur zone de confort, ce qui pourrait lui sembler restreindre leur potentiel d'aventure et de découverte.] Assure-toi que la section finale sur la perception opposée soit constructive et présente un équilibre entre les différentes perspectives."""

message_data.append( 
  {
    "role": "assistant", 
    "content": changements_text
  }
)
  
message_data.append(
    {
        "role": "user",
        "content": amicale_prompt
    }
)

amicale = generateur_texte(message_data, 350)

amicale_text = amicale.choices[0].message.content


#Section "Perception règles et convention sociale"

regles_prompt = """Je souhaite que tu crées une section 'Perception des règles et des conventions sociales' dans un **MAXIMUM DE 200 MOTS** qui décrit comment une personne perçoit et réagit aux règles, procédures, et conventions sociales, en se basant sur ses réponses du questionnaire de la question précédente et ses caractéristiques personnelles. Le texte doit être en plusieurs paragraphes, décrivant l'attitude générale de la personne envers les règles et les conventions, en mettant en avant son degré de flexibilité, son adhésion ou non aux normes, et son approche face à l'innovation et la créativité. Inclut un paragraphe final qui compare sa perception des règles avec une perception opposée. Décris comment la personne voit les règles et procédures – les perçoit-elle comme des guides flexibles ou des contraintes nécessaires ? Mentionne comment la personne interagit avec les conventions sociales, en se basant sur ses réponses concernant l'indépendance, l'innovation, et la conformité aux traditions. Pour la dernière partie du texte, au lieu de mentionner une dominance de couleur, mentionne une perception qui serait opposée à celle de la personne décrite. Par exemple, si la personne est flexible et innovante, mentionne que d'autres pourraient la percevoir comme rebelle ou indifférente, tandis qu'elle pourrait percevoir ces personnes comme trop rigides ou strictes. Utilise un ton engageant et nuancé, en restant réaliste et en soulignant les forces et les défis potentiels de la personne par rapport aux règles et conventions. Voici un exemple de ce que je souhaite obtenir : [Exemple 1 Monsieur Test perçoit les règles, les procédures, et les conventions sociales comme des éléments essentiels au bon fonctionnement de toute organisation ou communauté. Sa nature méthodique et organisée l'amène à valoriser la structure et la rigueur qu'apportent les règles. Pour lui, ces directives ne sont pas simplement des suggestions, mais des cadres nécessaires qui garantissent la qualité, l'ordre, et la prévisibilité dans les interactions et les processus. Il a tendance à suivre les normes établies avec précision, préférant s'appuyer sur des protocoles éprouvés plutôt que de se lancer dans des innovations hasardeuses./n Bien qu'il soit ouvert à l'idée de nouvelles approches, Monsieur Test croit fermement que toute innovation doit être soigneusement planifiée, structurée, et alignée avec les règles existantes pour être efficace. Son respect pour les conventions sociales est également fort : il considère que les traditions et les normes sociales jouent un rôle clé dans le maintien de l'harmonie et de la stabilité au sein des groupes./n À noter que certaines personnes pourraient percevoir l'attitude de Monsieur Test comme étant trop rigide ou peu flexible, ce qui pourrait leur sembler inhiber la créativité ou l'adaptabilité. En revanche, Monsieur Test pourrait percevoir ces personnes comme étant trop désorganisées ou insouciantes, ce qui pourrait lui sembler compromettre la qualité et la fiabilité des résultats./n Exemple 2 Madame Test perçoit les règles, les procédures, et les conventions sociales comme des cadres souvent trop restrictifs qui peuvent freiner l'innovation, la liberté, et l'expression personnelle. Son désir d'indépendance et sa tendance à privilégier la spontanéité la poussent à voir les règles comme des obstacles plutôt que comme des guides. Elle préfère une approche plus flexible et adaptable, où la créativité et l'initiative personnelle sont mises en avant./n Pour Madame Test, les conventions sociales ne devraient pas entraver la quête de nouvelles expériences et l'exploration de solutions originales. Elle est prête à remettre en question les normes établies si elle estime qu'elles limitent le potentiel de découverte ou d'amélioration. Elle valorise les environnements où elle peut exprimer ses idées sans être contrainte par des protocoles rigides, et où l'innovation est encouragée plutôt que restreinte./n À noter que certaines personnes pourraient percevoir l'attitude de Madame Test comme étant trop indépendante ou indifférente aux règles, ce qui pourrait leur sembler déstabilisant ou difficile à gérer. En revanche, Madame Test pourrait percevoir ces personnes comme étant trop rigides ou conformistes, ce qui pourrait lui sembler restreindre leur capacité à innover ou à s'adapter rapidement aux changements.]"""

message_data.append( 
  {
    "role": "assistant", 
    "content": amicale_text
  }
)
  
message_data.append(
    {
        "role": "user",
        "content": regles_prompt
    }
)

regles = generateur_texte(message_data, 350)

regles_text = regles.choices[0].message.content


#Section "Perception défis, problèmes et difficultés"

problemes_prompt = """Je souhaite que tu crées une section 'Perception des défis, problèmes et difficultés' dans un **MAXIMUM DE 200 MOTS** qui décrit comment une personne perçoit et gère les défis, les problèmes, et les difficultés, en se basant sur ses réponses du questionnaire DISC de la question précédente et ses caractéristiques personnelles. Le texte doit être en plusieurs paragraphes, décrivant l'attitude générale de la personne face aux défis, en mettant en avant son approche, ses forces, et ses éventuelles zones d'amélioration. Inclut un paragraphe final qui compare sa perception des défis avec une perception opposée. Décris comment la personne voit les défis – les perçoit-elle comme des opportunités d'apprentissage, des obstacles à surmonter, ou des situations stressantes ? Mentionne ses stratégies pour gérer les problèmes, comme l'analyse, la patience, ou la collaboration. Mentionne la manière dont la personne aborde les problèmes, en se basant sur ses réponses concernant l'impulsivité, la méthode, la tolérance au stress, et la collaboration. Aborde aussi ses préférences pour l'analyse ou l'action rapide. Pour la dernière partie du texte, au lieu de mentionner une dominance de couleur, mentionne une perception qui serait opposée à celle de la personne décrite. Par exemple, si la personne est prudente et méthodique, mentionne que d'autres pourraient la percevoir comme trop lente, tandis qu'elle pourrait percevoir ces personnes comme trop impulsives ou agressives. Utilise un ton engageant et nuancé, en restant réaliste et en soulignant les forces et les défis potentiels de la personne. Voici un exemple de ce que je souhaite obtenir : [Exemple 1 Madame Test perçoit les défis, les problèmes, et les difficultés comme des occasions de démontrer son audace, sa créativité, et sa capacité à prendre des décisions rapidement. Elle aborde ces situations avec un esprit entreprenant, préférant l'action immédiate à l'analyse prolongée. Pour elle, chaque obstacle est une chance de prouver son indépendance et de mettre en avant son esprit d'initiative. Elle n'hésite pas à se lancer dans l'inconnu, voyant dans les difficultés une opportunité d'explorer de nouvelles solutions et de repousser les limites établies./n Son approche est marquée par une volonté de maximiser les expériences positives, même dans les moments difficiles. Madame Test préfère une stratégie proactive, cherchant à surmonter les obstacles avec détermination et en gardant un regard optimiste sur l'issue. Elle valorise les solutions innovantes et n'a pas peur de remettre en question les méthodes traditionnelles si elle pense qu'une approche différente pourrait être plus efficace./n À noter que certaines personnes pourraient percevoir l'attitude de Madame Test comme étant trop impulsive ou risquée, ce qui pourrait leur sembler précipité ou imprudent. En revanche, Madame Test pourrait percevoir ces personnes comme étant trop prudentes ou lentes à réagir, ce qui pourrait lui sembler freiner la progression et limiter les opportunités d'innovation./n Exemple 2 Monsieur Test perçoit les défis, les problèmes, et les difficultés avec une approche analytique et méthodique. Il préfère prendre le temps d'examiner chaque situation en détail, en analysant les données et en évaluant les différentes options avant de prendre une décision. Pour lui, les défis ne sont pas des obstacles insurmontables, mais plutôt des puzzles à résoudre avec rigueur et précision. Cette approche lui permet de trouver des solutions durables et bien pensées, minimisant les risques d'erreurs ou de conséquences imprévues./n Monsieur Test valorise la stabilité et la sécurité dans la résolution des problèmes. Il s'assure que chaque action prise est bien fondée et alignée avec les normes et procédures établies. Il évite les solutions hâtives et privilégie une planification minutieuse pour garantir que les défis sont gérés de manière efficace et fiable. Bien qu'il soit patient et tolérant face aux situations complexes, sa préférence pour l'analyse approfondie peut parfois le rendre plus lent à réagir, surtout dans des situations nécessitant une action rapide./n À noter que certaines personnes pourraient percevoir l'attitude de Monsieur Test comme étant trop rigide ou lent à agir, ce qui pourrait leur sembler inhiber la réactivité ou l'innovation. En revanche, Monsieur Test pourrait percevoir ces personnes comme étant trop impulsives ou désorganisées, ce qui pourrait lui sembler compromettre la qualité et la fiabilité des résultats.] Assure-toi que la section finale sur la perception opposée soit constructive et présente un équilibre entre les différentes perspectives."""

message_data.append( 
  {
    "role": "assistant", 
    "content": regles_text
  }
)
  
message_data.append(
    {
        "role": "user",
        "content": problemes_prompt
    }
)

problemes = generateur_texte(message_data, 350)

problemes_text = problemes.choices[0].message.content



print(bref_text)

print(forces_text)

print(defis_text)

print(changements_text)

print(amicale_text)

print(regles_text)

print(problemes_text)