import csv
from decimal import Decimal
import os


def recuperation_csv(fichier_csv):
    liste_actions = []
    actions_supprimer = []
    with open(fichier_csv, "r") as f:
        lecture_csv = csv.reader(f, delimiter=",")
        next(lecture_csv)
        for ligne in lecture_csv:
            if Decimal(ligne[1]) <= Decimal("0"):
                actions_supprimer.append(ligne)
            else:
                liste_actions.append(ligne)
        return liste_actions, actions_supprimer


def calcul_benefice(cout, pourcentage):
    pourcentage = pourcentage / Decimal("100")
    return pourcentage * cout


def affichage_liste_action(assemblage, meilleur_benefice, cout_total, action_supprimer):
    print(f"Voici la liste des actions qui sont supprimées en raison de leurs cout négatif ou nul:")
    for i in range(len(action_supprimer)):
        print(f"{action_supprimer[i][0]} - cout: {action_supprimer[i][1]} benefice: {action_supprimer[i][2]}")
    print(f"\nVoici la meilleur combinaison d'action pour un maximum de {cout_total}€ d'investissement sur 2 ans:")
    for j in range(len(assemblage)):
        print(f"{assemblage[j][0]} - cout: {assemblage[j][1]} benefice: {assemblage[j][2]}")
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
    cout_total = Decimal("0")
    cout = Decimal(limite_cout)
    for j in range(nombre_actions, 0, -1):
        action = liste_actions[j -1]
        cout_j = Decimal(action[1])

        if dp[j][int(cout)] != dp[j - 1][int(cout)]:
            assemblage.append(action)
            cout_total += cout_j
            cout -= cout_j
    return assemblage, benefice_max, cout_total


def main(nom_csv):
    chemin = os.path.dirname(os.path.abspath(__file__))
    fichier_csv = os.path.join(chemin, nom_csv)
    liste_actions, actions_supprimer = recuperation_csv(fichier_csv)
    limite_cout = 500
    meilleur_actions, benefice_max, cout_total = meilleur_combinaison_actions(liste_actions, limite_cout)
    affichage_liste_action(meilleur_actions, benefice_max, cout_total, actions_supprimer)


nom_csv = "dataset1.csv"
#  nom_csv = "dataset2.csv"

main(nom_csv)