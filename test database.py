import os
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
from openai import OpenAI
from openai.types import Completion, CompletionChoice, CompletionUsage
import textwrap



  
#code pour automatisation, activation lors de réception d'un nouveau formulaire

#NOM

nom = "Elsa, Chabanel"

#DONNÉES EXCEL
#Pour le client
synergia = pd.read_excel("C:/Users/Guillaume Cloutier/OneDrive/Synergia/Synergia.xlsx", sheet_name="Réponses 3")

synergia_nom = pd.DataFrame(synergia.loc[synergia["Nom"]== nom])

plage_nom = synergia_nom.iloc[:,2]
plage_questions1_11 = synergia_nom.iloc[:,6:50]
plage_questions17_20 = synergia_nom.iloc[:,62:78]
plage_questions1_20 = synergia_nom.iloc[:,6:78]
plage_questions12_14 = synergia_nom.iloc[:,50:62]
plage_questions15_16 = synergia_nom.iloc[:,105:114]
plage_questions_dev1 = synergia_nom.iloc[:,103:105]
plage_questions_dev2 = synergia_nom.iloc[:,114]
plage_questions_complet = synergia_nom.iloc[:,6:115]

#section 1
synergia_section1= pd.concat([plage_nom, plage_questions1_11, plage_questions17_20], axis=1)

synergia_section1_transposed = synergia_section1.transpose()

synergia_section1_string = synergia_section1_transposed.to_string(header=False)

#section 2
synergia_section2 = pd.concat([plage_nom, plage_questions1_20], axis = 1)

synergia_section2_transposed = synergia_section2.transpose()

synergia_section2_string = synergia_section2_transposed.to_string(header=False)

#motivation
synergia_section_motivation= pd.concat([plage_nom, plage_questions1_20, plage_questions15_16, plage_questions_dev1, plage_questions_dev2], axis=1)

synergia_section_motivation_transposed = synergia_section_motivation.transpose()

synergia_section_motivation_string = synergia_section_motivation_transposed.to_string(header=False)


#couple

#complet


#Pour le model 1

synergia_model1 = synergia.iloc[[92]]

plage_model1 = synergia_model1.iloc[:,2]
plage_model1_questions1_11 = synergia_model1.iloc[:,6:50]
plage_model1_questions17_20 = synergia_model1.iloc[:,62:78]

synergia_model1_section1= pd.concat([plage_model1, plage_model1_questions1_11, plage_model1_questions17_20], axis=1)

synergia_model1_section1_transposed = synergia_model1_section1.transpose()

synergia_model1_section1_string = synergia_model1_section1_transposed.to_string(header=False)

#Pour le model 2

synergia_model2 = synergia.iloc[[88]]

plage_model2 = synergia_model2.iloc[:,2]
plage_model2_questions1_11 = synergia_model2.iloc[:,6:50]
plage_model2_questions17_20 = synergia_model2.iloc[:,62:78]

synergia_model2_section1= pd.concat([plage_model2, plage_model2_questions1_11, plage_model2_questions17_20], axis=1)

synergia_model2_section1_transposed = synergia_model2_section1.transpose()

synergia_model2_section1_string = synergia_model2_section1_transposed.to_string(header=False)

#Pour Schwartz

print(synergia_section_motivation_string)

# Charger un onglet spécifique d'un fichier Excel
#df = pd.read_excel('votre_fichier.xlsx', sheet_name='Nom_de_la_feuille')

# Vous pouvez également accéder à une plage de colonnes
#colonnes_range = df.iloc[:, 1:3]  # Accède à la deuxième et troisième colonne

# Combiner les deux plages en un seul DataFrame
#colonnes_range = pd.concat([plage_1, plage_2], axis=1)