import os
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
pd.set_option('future.no_silent_downcasting', True)
from openai import OpenAI
from openai.types import Completion, CompletionChoice, CompletionUsage
import textwrap



  
#code pour automatisation, activation lors de réception d'un nouveau formulaire

#NOM

nom = "Veillette, Joanie"

#DONNÉES EXCEL

#Pour trouver les data du client
synergia = pd.read_excel("C:/Users/Guillaume Cloutier/OneDrive/Synergia/Synergia.xlsx", sheet_name="synergia_mlm")

synergia_nom = pd.DataFrame(synergia.loc[synergia["Nom"]== nom])

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


print(bleu)
print(rouge)
print(jaune)
print(vert)
print(explorateur)
print(protecteur)
print(bouffon)
print(souverain)
print(magicien)
print(createur)
print(hero)
print(citoyen)
print(sage)
print(amant)
print(rebelle)
print(optimiste)