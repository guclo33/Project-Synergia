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


print(synergia_model2_section1_string)

