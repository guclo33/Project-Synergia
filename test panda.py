import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

synergia = pd.read_excel("C:/Users/Guillaume Cloutier/OneDrive/Synergia/Synergia.xlsx")

ligne = synergia.iloc[[0]]




ligne2 = synergia.loc[synergia['Nom'] == 'Laurie, Jutras']

ligne2_df = pd.DataFrame(ligne2)

nom= "Maxime, Pépin"

synergia_nom = pd.DataFrame(synergia.loc[synergia["Nom"]== nom])

print(synergia_nom)