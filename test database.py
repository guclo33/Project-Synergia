import os
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
from openai import OpenAI
from openai.types import Completion, CompletionChoice, CompletionUsage
import textwrap



  
#code pour automatisation, activation lors de réception d'un nouveau formulaire

#NOM

nom = "Patrice, Simard"

#DONNÉES EXCEL

#Pour le client
synergia = pd.read_excel("C:/Users/Guillaume Cloutier/OneDrive/Synergia/Synergia.xlsx", sheet_name="Réponses 3")

synergia_nom = pd.DataFrame(synergia.loc[synergia["Nom"]== nom])

plage_nom = synergia_nom.iloc[:,2:3]
plage_questions1_11 = synergia_nom.iloc[:,6:50]
plage_questions17_20 = synergia_nom.iloc[:,62:78]
plage_questions1_20 = synergia_nom.iloc[:,6:78]
plage_questions12_14 = synergia_nom.iloc[:,50:62]
plage_questions15_16 = synergia_nom.iloc[:,106:114]
plage_questions_dev1 = synergia_nom.iloc[:,104:106]
plage_questions_dev2 = synergia_nom.iloc[:,115:116]
plage_questions_complet = synergia_nom.iloc[:,6:115]
plage_questions21_26 = synergia_nom.iloc[:,78:102]

#section 1
synergia_section1= pd.concat([plage_nom, plage_questions1_11, plage_questions17_20], axis=1)

synergia_section1_transposed = synergia_section1.transpose()

synergia_section1_string = synergia_section1_transposed.to_string(header=False)

#section 2
synergia_section2 = pd.concat([plage_nom, plage_questions1_20], axis = 1)

synergia_section2_transposed = synergia_section2.transpose()

synergia_section2_string = synergia_section2_transposed.to_string(header=False)

#motivation
synergia_section_motivation= pd.concat([plage_nom, plage_questions1_20, plage_questions15_16], axis=1)

synergia_section_motivation_transposed = synergia_section_motivation.transpose()


synergia_section_motivation_string = synergia_section_motivation_transposed.to_string(header=False, max_colwidth = None)



#couple
synergia_section_couple= pd.concat([plage_nom, plage_questions21_26], axis=1)

synergia_section_couple_transposed = synergia_section_couple.transpose()

synergia_section_couple_string = synergia_section_couple_transposed.to_string(header=False)


#question developpement

synergia_section_dev = pd.concat([plage_nom, plage_questions_dev1, plage_questions_dev2], axis = 1)

synergia_section_dev_transposed = synergia_section_dev.transpose()

synergia_section_dev_string = synergia_section_dev_transposed.to_string(header=False)

pd.set_option('display.max_colwidth', None)



nom_organisateur = synergia_nom.iloc[0, 4]

print(nom_organisateur)


# Charger un onglet spécifique d'un fichier Excel
#df = pd.read_excel('votre_fichier.xlsx', sheet_name='Nom_de_la_feuille')

# Vous pouvez également accéder à une plage de colonnes
#colonnes_range = df.iloc[:, 1:3]  # Accède à la deuxième et troisième colonne

# Combiner les deux plages en un seul DataFrame
#colonnes_range = pd.concat([plage_1, plage_2], axis=1)