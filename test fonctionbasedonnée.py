import pandas as pd

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
explorateur = moyenne(66, 78, 90)
protecteur = moyenne(70, 79, 91)
bouffon = moyenne(68, 80, 92)
souverain = moyenne(69, 77, 93)
magicien = moyenne(67, 82, 98)
createur = moyenne(71, 87, 95)
hero = moyenne(72, 84,96)
citoyen = moyenne(73, 85, 97)
sage = moyenne(74, 86, 94)
amant = moyenne(75, 83, 99)
rebelle = moyenne(76, 88, 100)
optimiste = moyenne(81, 89, 101)

print(optimiste)

