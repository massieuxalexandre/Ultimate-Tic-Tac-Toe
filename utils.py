# clear l'affichage dans le terminal, pour voir une grille à la fois (celle en cours)
def clear():
    for _ in range(100):
        print()

# vérifier si le choix de l'utilisateur est valide ou non
def valid_choice(choice, start, end):
    # liste des choix possible (convertis en string car l'input attendu est en string)
    arr = list()
    for i in range(start, end+1):
        arr.append(str(i))

    # puis on regarde si le choix de l'utilisateur fais bien parti du bornage attendu
    return choice in arr

