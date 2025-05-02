import csv
from decimal import Decimal
from itertools import combinations
import re
import os


def recuperation_csv(fichier_csv):
    liste_actions = []
    with open(fichier_csv, "r") as f:
        lecture_csv = csv.reader(f, delimiter=",")
        next(lecture_csv)
        for ligne in lecture_csv:
            element_modifier = re.sub("%", "", ligne[2])
            ligne[2] = element_modifier
            liste_actions.append(ligne)
        return liste_actions


def calcul_benefice(cout, pourcentage):
    pourcentage = pourcentage / Decimal("100")
    return pourcentage * cout


def affichage_liste_action(assemblage, meilleur_benefice):
    print("Voici la meilleur combinaison d'action pour un maximum de 500€ d'investissement sur 2ans:")
    for i in range(len(assemblage)):
        print(assemblage[i])
    print(f"Bénéfice: {meilleur_benefice}")


def meilleur_combinaison_actions(liste_actions, limite_cout):
    nombre_actions = len(liste_actions)
    dp = [[Decimal("0") for _ in range(limite_cout + 1)] for _ in range(nombre_actions + 1)]
    
    for i in range(1, nombre_actions + 1):
        action = liste_actions[i - 1]
        cout_i = Decimal(action[1])
        pourcentage_i = Decimal(action[2])
        benefice_i = calcul_benefice(cout_i, pourcentage_i)

        for cout in range(limite_cout + 1):
            if cout_i > cout:
                dp[i][cout] = dp[i - 1][cout]
            else:
                dp[i][cout] = max(dp[i - 1][cout], benefice_i + dp[i -1][int(cout - cout_i)])
    benefice_max = dp[nombre_actions][limite_cout]
    
    assemblage = []
    cout = Decimal(limite_cout)
    for j in range(nombre_actions, 0, -1):
        action = liste_actions[j -1]
        cout_j = Decimal(action[1])

        if dp[j][int(cout)] != dp[j - 1][int(cout)]:
            assemblage.append(action)
            cout -= cout_j
    return assemblage, benefice_max


def main():
    fichier_csv = os.path.join("Liste_actions.csv")
    liste_actions = recuperation_csv(fichier_csv)
    limite_cout = 500
    meilleur_actions, benefice_max = meilleur_combinaison_actions(liste_actions, limite_cout)
    affichage_liste_action(meilleur_actions, benefice_max)


main()