import pandas as pd

nom = "Maxime, Pépin"

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


def excel_to_string(*args):
  return pd.concat(args, axis=1).transpose().to_string(header=False)



#section 1
synergia_section1= pd.concat([plage_nom, plage_questions1_11, plage_questions17_20], axis=1)

synergia_section1_transposed = synergia_section1.transpose()

synergia_section1_string = synergia_section1_transposed.to_string(header=False)


print(synergia_section1_string)

print(excel_to_string(plage_nom, plage_questions1_11, plage_questions17_20))