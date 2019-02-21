# coding: utf-8
# Programme realise dans le cadre d un mini Projet en cours d ISN au lycee Montesquieu
# Auteurs : HAMADI Mohand & MINEL Charlie
# Objectif : ---------------------------------------------------------------------------------------------
###################################### Fichier principale ################################################
# Ce fichier contient toutes les fenetres de l interface du logiciel
############################################
# L interface est compose de 2 fenetres principales :
#       - L une acceuil qui permettra de voir les derniers depenses du mois, le solde disponible, et les gains depuis
#           le mois precedent
#       - La second permettra d ajouter une transaction
############################################
# Ce fichier contient egalement les fenetres qui permettront d afficher des diagrammes pour voir la repartition
#   des depenses en fontion des categories
#########################################################################################################
# Ameliorations possibles :
#          - Utiliser des fonctions constructeurs de python et les modifiers ex : la fonction gerant l affichage pour automatiser celui des bouttons....
#          - Sauvegarder le gain de chaque mois pour voir comment il evolue
#          - /!\ Mieux gérer les zones de saisie...
#          - Permettre de consulter toutes les transactions entrees en fonction de chaque mois
#          - Securiser l acces au programme
#          - Chiffrer la sauvegarde des transactions

import pygame  # importation des modules
import os
import datetime
import pickle
from random import randint

# Def constantes :
whiteCouleur = (255, 255, 255)
blackCouleur = (0, 0, 0)
redCouleur = (146, 43, 33)
greenCouleur = (30, 132, 73)
orangeCouleur = (211, 84, 0)
greyCouleur = (171, 178, 185)
bleuFond = (33, 47, 61)
lscreen, hscreen = 1100, 720
lettre = []
chiffre = []
tPolice = 40  # Taille police principal
tPolice2 = 35
tMiseAv = 60
lMoyenneRale = 13.66  # largueur moyen d un caractere de la police raleway

for k in range(97, 265):
    lettre.append(chr(k))
for k in range(256, 266):
    chiffre.append(k)


class SurfacePerso():
    """
        Classe permettant de definir une "surface", permet de creer des "zones" afin de hierarchiser
        l organisation des differents elements
    """

    def __init__(self, ecran, posX, posY, longueur, hauteur):
        """
            Initialise la classe surface
            posX,posY : correspond a la position du point dans la surface parent
            longueur,hauteur : correspond aux dimensions de la surface
        """
        self.origineX = posX
        self.origineY = posY
        self.l = longueur
        self.h = hauteur
        self.dim = (self.l, self.h)
        self.coor = (self.origineX, self.origineY)
        self.ecran = ecran


class Button():
    """
        Classe permettant de creer un boutton. Nous definissons les bouttons comme etant des surfaces.
    """

    def __init__(self, surface, posBouttonX=0, posBouttonY=0, lBoutton=200, hBoutton=30):
        """
            Initialise la classe boutton.
            surface : correspond a la surface parent a laquel il doit etre associe
            texte : texte contenu dans le bouton
            action : commande realise lorsque l utilisateur clic sur le bouton
            longueur, hauteur : longueur et hauteur qu occupera le bouton
        """
        self.surfaceParent = surface
        # def des coordonnees du boutton
        self.posX = posBouttonX
        self.posY = posBouttonY
        self.posBoutton = (self.surfaceParent.origineX + self.posX, self.surfaceParent.origineY + self.posY)

        # def des dimensions du boutton
        if lBoutton == 200:
            self.dim = (self.surfaceParent.l - 5, hBoutton)
        else:
            self.dim = (lBoutton, hBoutton)
        # def rect du boutton
        self.rectBoutton = pygame.Rect(self.posBoutton, self.dim)

    def afficherBoutton(self, texte="", entryBox=False, lMessage=30, Type=0):
        """
            Cette fonction permet d afficher un boutton a l ecran.
            lMessage -> Sers uniquement s il s agit d une entryBox....
            texte -> texte par default du boutton
            entryBox -> True si l on souhaite pouvoir taper du texte, False s il s agit juste d un boutton
            Type -> Definie les autorisations de saisie : 0 -> Tout
                                                          1 -> Lettres + Virgule
                                                          2 -> Chiffres
                                                          3 -> Chiffres + Virgule
        """
        self.msg = texte
        self.lenmax = lMessage

        if entryBox == True:
            get = True
            while get:
                for event in pygame.event.get():
                    quit = self.rectBoutton.collidepoint(
                        pygame.mouse.get_pos()) == False and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                    if quit:
                        get = False

                    if event.type == pygame.KEYDOWN:
                        if pygame.key.name(event.key) == "escape" or pygame.key.name(event.key) == "tab":
                            get = False

                        if pygame.key.name(event.key) in lettre and len(
                                self.msg) < self.lenmax and Type == 0 or Type == 1:
                            self.msg = self.msg + str(pygame.key.name(event.key))

                        elif pygame.key.name(event.key) == "space" and len(
                                self.msg) < self.lenmax and Type == 0 or Type == 1:
                            self.msg = self.msg + " "  # On traite les espaces

                        elif pygame.key.name(event.key) == "backspace":
                            self.msg = self.msg[:-1]  # On efface le dernier element de la chaine de caractere.

                        elif pygame.key.name(event.key) == "," and len(
                                self.msg) < self.lenmax and Type == 0 or pygame.key.name(
                            event.key) == "," and Type == 1 and len(self.msg) < self.lenmax or pygame.key.name(
                            event.key) == "," and Type == 3 and len(self.msg) < self.lenmax:
                            self.msg += ','  # On gere la virgule.
                            test = 0
                            for k in range(0, len(self.msg)):
                                if self.msg[k] == ",":
                                    test += 1
                            if test > 1:
                                self.msg = self.msg[:-1]

                        elif event.key in chiffre and len(
                                self.msg) < self.lenmax and Type == 2 or event.key in chiffre and len(
                            self.msg) < self.lenmax and Type == 3:  # Pygame reference les touches avec des nombres, et  les nombres croient en meme temps que les chiffres
                            # un ecart de 208.... puis on recupere le code ASCII
                            self.msg += chr(event.key - 208)

                        pygame.draw.rect(self.surfaceParent.ecran, interfaceCouleur,
                                         self.rectBoutton)  # Permet de repasser sur l ecran d avant de permettre d effacer correctement
                        msgBoutton = policePrin.render(self.msg, 1, blackCouleur)
                        self.textPos = msgBoutton.get_rect()
                        self.rectBoutton.width = self.textPos.width
                        if self.rectBoutton.width < 20: self.rectBoutton.width = self.dim[
                            0]  # Car sinon je boutton devient "inexistant" et on ne peut plus le selectionner....
                        pygame.draw.rect(self.surfaceParent.ecran, greyCouleur,
                                         self.rectBoutton)  # Permet de donner le fond
                        self.textPos.center = self.rectBoutton.center
                        self.surfaceParent.ecran.blit(msgBoutton, (self.posBoutton))
                        pygame.display.flip()
        else:
            self.msg = texte
            pygame.draw.rect(self.surfaceParent.ecran, greyCouleur, self.rectBoutton)  # Afficher le boutton
            msgBoutton = policePrin.render(self.msg, 1, blackCouleur)  # Afficher le texte du boutton
            #### Positionnement via les coordonnees du rect du cadre du bouton
            self.textPos = msgBoutton.get_rect()
            self.textPos.center = self.rectBoutton.center  # Le centre du Texte = centre du boutton
            self.surfaceParent.ecran.blit(msgBoutton, (
                self.textPos))  # Collage a l ecran (actualisation effectue juste avant la boucle d initialisation)

    def bouttonOn(self, event):
        """
            Cette fonction permet d activer le boutton en le rendant 'cliquable' et en effectuant l action demander
        """
        self.on = self.rectBoutton.collidepoint(
            pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
        return self.on


class Transaction():
    """
        On va definir chaque transaction comme etant un objet, que l on pourra ainsi sauvegarder facilement dans un fichier
    """

    def __init__(self, type, montant, date, categorie, raison):
        """
        :param type: boolean, 0-> depense, 1-> gain
        :param montant: montant de la transaction (toujours positif, type definie si + ou -)
        :param date: date de la transaction
        :param categorie: categorie appartenant a la liste
        :param raison: quelques mots de justification
        """
        self.type = type
        if type < 0:
            self.montant = - montant
        else:
            self.montant = montant
        self.date = date
        self.cat = categorie
        self.raison = raison

    def sauvegarde(self):
        """
            Cette fonction permet d enregistrer la transaction dans un fichier binaire, afin de le recuperer en tant
            qu objet.
        """
        urlDossier = "ressources/save/" + str(self.date.year) + "/" + str(self.date.month)
        urlFichier = "ressources/save/" + str(self.date.year) + "/" + str(self.date.month) + "/" + str(self.date.day)

        exist = os.path.exists(urlFichier)
        if exist == True:
            urlFichier = urlFichier + "_"
            k = 1
            while exist == True:
                urlTest = urlFichier + str(k)
                exist = os.path.exists(urlTest)
                k += 1
            urlFichier = urlTest

        if os.path.exists(urlDossier) == False:
            os.makedirs(urlDossier)

        with open(urlFichier, "wb") as file:
            transaction = pickle.Pickler(file)
            transaction.dump(self)


class User():
    def __init__(self, nom, prenom, solde):
        self.nom = nom
        self.name = prenom
        self.solde = solde

    def sauvegarde(self):
        with open("ressources/user", "wb") as file:
            user = pickle.Pickler(file)
            user.dump(self)


def setCouleurInterface():
    heure = datetime.datetime.now().hour
    if 18 < heure or heure < 8:
        interfaceCouleur = bleuFond
    else:
        interfaceCouleur = whiteCouleur
    return interfaceCouleur


def recupTransaction(mois=datetime.datetime.now().month, year=datetime.datetime.now().year):
    """
        Cette fonction va permettre de recuperer les transaction realises durant un mois.
        :param mois: mois dont l on souhaite connaitre les transactions realises
        :return: liste de toutes les transactions (objets de la classe Transaction)
    """
    listTrans = []  # liste retourne
    urlDir = "ressources/save/" + str(year) + "/" + str(mois)  # emplacement ou l on souhaite prendre les dates
    if os.path.exists(urlDir) == False:
        return listTrans
    i = 1
    while i < 32:  # 1 mois = max 31j donc i ne doit pas depasser 32 (pour pouvoir aller jusque 31
        urlFichier = urlDir + "/" + str(i)
        if os.path.exists(urlFichier) == True:  # Si le fichier exist alors on l ouvre
            with open(urlFichier, "rb") as file:
                transaction = pickle.Unpickler(file)  # recuperation de l objet
                transaction = transaction.load()
                listTrans.append(transaction)  # ajout de l objet a la liste

                # si plusieurs transactions sont effectues le meme jour, on ajoute un "_" suivis d un nombre
                # partant de 1 pour differencier les fichiers, donc on va tester l existance de ces sous transactions
                # et les ajouter a la liste si elles existent bien
            urlSousFichier = urlFichier
            k = 1
            while os.path.exists(urlSousFichier) == True:
                # Si le fichier ouvert avant exite j augmente k de 1 pour le tester
                urlSousFichier = urlFichier + "_" + str(k)
                # On utilise urlFichier pour ne pas ajouter le _(k) dessus, sinon on chercherai des fichiers tel que : XXXX_k1_k2_k3
                if os.path.exists(urlSousFichier) == True:
                    with open(urlSousFichier, "rb") as file:
                        sousTransaction = pickle.Unpickler(file)
                        sousTransaction = sousTransaction.load()
                        listTrans.append(sousTransaction)
                    k += 1
            i += 1
        else:
            i += 1
    return listTrans


def getUserName():
    with open("ressources/user", "rb") as file:
        fichier = pickle.Unpickler(file)
        objet = fichier.load()
        name = objet.name + " " + objet.nom
        return name


def getSolde():
    """
        Cette fonction va nous permettre de calculer le solde actuel
        :return: solde actuel
    """
    with open("ressources/user", "rb") as file:
        fichier = pickle.Unpickler(file)
        objet = fichier.load()
        solde = objet.solde

    # On recup le solde entre par l utilisateur au debut

    mois = datetime.datetime.now().month
    annee = datetime.datetime.now().year

    while annee > 2018:
        if recupTransaction(mois, annee) != []:
            for k in recupTransaction(mois, annee):
                if k.type == True:
                    solde -= k.montant
                else:
                    solde += k.montant
        if mois - 1 == 0:
            annee = datetime.datetime.now().year - 1
            mois = 12
        else:
            mois = mois - 1
            annee = annee

    return solde


def printSolde():
    # Afficher le solde
    solde = getSolde()
    if solde > 0:
        solde = "Solde:" + " " + str(solde) + "€"
        solde = policePrin.render(solde, 1, greenCouleur)
    else:
        solde = "Solde:" + " " + str(solde) + "€"
        solde = policePrin.render(solde, 1, redCouleur)
    rectSolde = solde.get_rect()
    rectSolde.x = lscreen - rectSolde.w
    screen.blit(solde, rectSolde)


def callCategorie():
    """
        cette fonction va permettre de recuperer la liste des categories stocker dans un jolie fichier
    :return:
    """
    url = "ressources/categories"
    if os.path.exists(url) == False:
        return []
    else:
        with open(url, "rb") as file:
            objet = pickle.Unpickler(file)
            cat = objet.load()
            return cat


def creatCategorie(NouvelleCategorie):
    liste = callCategorie()
    with open(url, "wb") as file:
        liste.append(NouvelleCategorie)
        objetSav = pickle.Pickler(file)
        objetSav.dump(liste)


def salutUtilisateur():
    heure = datetime.datetime.now()
    userName = getUserName()
    if heure.hour > 19:
        nameMsg = "Bonsoir " + str(userName) + ","
    else:
        nameMsg = "Bienvenue " + str(userName) + ","
    userName = policePrin.render(nameMsg, 1, blackCouleur)
    screen.blit(userName, (0, 0))


def afficherChoixBoutton(Button, etatInitial):
    if etatInitial == True:
        etat = False
        rectSelection = pygame.Rect(Button.posX + 80 - 20, Button.posY, 30, Button.dim[1])
        rectPrecedant = pygame.Rect(Button.posX, Button.posY, 30, Button.dim[1])
    if etatInitial == False:
        etat = True
        rectSelection = pygame.Rect(Button.posX, Button.posY, 30, Button.dim[1])
        rectPrecedant = pygame.Rect(Button.posX + 80 - 20, Button.posY, 30, Button.dim[1])
    pygame.draw.rect(screen, greyCouleur, rectPrecedant)
    pygame.draw.rect(screen, greenCouleur, rectSelection)
    pygame.display.flip()
    return etat


def modifCat(ajouter, compteur, categorie):
    listCat = callCategorie()
    if ajouter == True and compteur < (len(listCat)-1):
        compteur += 1
        pygame.draw.rect(screen, interfaceCouleur, categorie.rectBoutton)
        categorie.afficherBoutton(texte=listCat[compteur])
        pygame.display.update()
        return compteur
    elif ajouter == False and compteur > 0:
        compteur -= 1
        pygame.draw.rect(screen, interfaceCouleur, categorie.rectBoutton)
        categorie.afficherBoutton(texte=listCat[compteur])
        pygame.display.update()
        return compteur
    else:
        return compteur


def confirmEnregistrerTrans(numAffiche, annee, mois, jour, euro, raison, depense, listCat):
    maCat = listCat[numAffiche]
    date = datetime.date(int(annee.msg), int(mois.msg), int(jour.msg))
    partieEuro = ""
    partieCentimes = ""
    compteur = 0
    while compteur < len(euro.msg) and euro.msg[compteur] != ",":
        partieEuro = partieEuro + euro.msg[compteur]
        compteur += 1

    while compteur + 1 < len(euro.msg):
        compteur += 1  # On le met avant car on veut tout de suite elimer la virgule
        partieCentimes = partieCentimes + euro.msg[compteur]

    if partieCentimes == "":
        centime = 0
    else:
        centime = int(partieCentimes) * (10 ** (-len(partieCentimes)))

    montant = int(partieEuro) + centime

    if montant > 0 and raison.msg != "":
        maTransaction = Transaction(depense, montant, date, maCat, raison.msg)
        maTransaction.sauvegarde()
        pygame.time.wait(1000)
        Acceuil()


def nouvelUser(boxNom, boxPrenom, boxSolde):
    partieEuro = ""
    partieCentimes = ""
    compteur = 0
    pasDeVirgule = False
    while compteur < len(boxSolde.msg) and boxSolde.msg[compteur] != ",":
        partieEuro = partieEuro + boxSolde.msg[compteur]
        compteur += 1

    while compteur + 1 < len(boxSolde.msg):
        compteur += 1  # On le met avant car on veut tout de suite elimer la virgule
        print(compteur)
        print(len(boxSolde.msg))
        partieCentimes = partieCentimes + boxSolde.msg[compteur]

    if partieCentimes == "":
        centime = 0
    else:
        centime = int(partieCentimes) * (10 ** (-len(partieCentimes)))

    montant = int(partieEuro) + centime
    print(montant)
    utilisateur = User(boxNom.msg, boxPrenom.msg, montant)
    utilisateur.sauvegarde()


def afficherInstructions(boxSolde):
    texte = "Bienvenue, pour saisir les informations cliquez sur les boutons, pensez a cliquer en dehors "
    texte = policeSecon.render(texte, True, blackCouleur)
    screen.blit(texte, (0, boxSolde.posBoutton[1] + boxSolde.dim[1] + 50))

    texte = "de la zone du boutton pour pouvoir effectuer d autres actions par la suite."
    texte = policeSecon.render(texte, True, blackCouleur)
    screen.blit(texte, (0, boxSolde.posBoutton[1] + boxSolde.dim[1] + 50 + tPolice2))

    texte = "Les majuscules et la ponctuation autre que la virgule ne sont pas disponible."
    texte = policeSecon.render(texte, True, blackCouleur)
    screen.blit(texte, (0, boxSolde.posBoutton[1] + boxSolde.dim[1] + 50 + 2 * tPolice2))

    texte = "La saisie de chiffre ne peut se faire que depuis un pave numerique, veuillez utiliser la virgule "
    texte = policeSecon.render(texte, True, blackCouleur)
    screen.blit(texte, (0, boxSolde.posBoutton[1] + boxSolde.dim[1] + 50 + 3 * tPolice2))

    texte = "pour separer les euros des centimes."
    texte = policeSecon.render(texte, True, blackCouleur)
    screen.blit(texte, (0, boxSolde.posBoutton[1] + boxSolde.dim[1] + 50 + 4 * tPolice2))


def diagramme():
    pygame.display.set_caption("Analyse")
    screen.fill(interfaceCouleur)  # On efface l ecran

    listCategorie = callCategorie()  # on recupere toutes les categories
    listCouleurCat = []  # list des couleurs qui seront associe a chaque categorie
    listeTransaction = recupTransaction()  # list de toutes les transactions
    listeDepenses = []  # list des transactions qui sont une depenses
    listeDepenseCat = []  # list du solde par categorie
    depenseTotal = 0  # total de nos depenses
    longueur, largueur = lscreen, 200
    xRect, yRect = 0, hscreen / 6
    xTexte, yTexte = 0, yRect + largueur + 50

    surfaceBouttonRetour = SurfacePerso(screen,lscreen - 210, hscreen - 35, 210,200)

    titre = policeMiseAv.render("Statistiques des depenses", True, blackCouleur)
    rectTitre = titre.get_rect()
    screen.blit(titre, (lscreen / 2 - rectTitre.w / 2, 0))

    if listeTransaction == []:
        message = policePrin.render("-- Aucune transactions ce mois ci --", True, blackCouleur)
        rectMessage = message.get_rect()
        screen.blit(message, (lscreen / 2 - rectMessage.w / 2, hscreen / 2))
    else:
        print("liste non vide")
        for categorie in range(0, len(listCategorie)):
            # on cree une couleur par categorie de facon aleatoire
            couleur = (randint(0, 255), randint(0, 255), randint(0, 255))
            listCouleurCat.append(couleur)
            listeDepenseCat.append(0)

        for trans in listeTransaction:
            if trans.type == True:
                listeDepenses.append(trans)
                depenseTotal += trans.montant

        for depense in listeDepenses:
            compteur = 0  # permettra de faire tourner des boucles
            trie = False
            while trie == False:
                if depense.cat == listCategorie[compteur]:
                    listeDepenseCat[compteur] += depense.montant / depenseTotal
                    trie = True
                else:
                    compteur += 1

        for categorie in range(0, len(listCategorie)):
            rectCategorie = pygame.Rect(xRect, yRect, longueur * listeDepenseCat[categorie], largueur)
            rectangle = pygame.draw.rect(screen, listCouleurCat[categorie], rectCategorie)
            xRect += longueur * listeDepenseCat[categorie]
            legendeCat = policePrin.render(
                listCategorie[categorie] + ": " + str(100 * listeDepenseCat[categorie]) + "%",
                True, listCouleurCat[categorie])
            screen.blit(legendeCat, (xTexte, yTexte))
            yTexte += tPolice + 5

    retour = Button(surfaceBouttonRetour)
    retour.afficherBoutton(texte="Retour")

    pygame.display.update()
    launched = True
    while launched == True:
        for event in pygame.event.get():
            QuitPrgm = event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE

            if QuitPrgm == True:
                launched = False
                pygame.quit()
                quit()

            if retour.bouttonOn(event):
                Acceuil()


def addT():
    """
        Fenetre permettant d ajouter une transaction
    """
    pygame.display.set_caption("Ajouter une transaction")
    screen.fill(interfaceCouleur)  # On efface l ecran

    printSolde()  # Afficher le solde

    # Def des differentes surfaces de l interface.
    colonneDroite = SurfacePerso(screen, lscreen - 420, 0, 200, hscreen)  # On definit la colonne de droite
    colonneGauche = SurfacePerso(screen, 10, 0, lscreen - (colonneDroite.l + 5), hscreen)

    ################################## Entrer Date #####################################################################
    # Text a gauche
    saisirDate = policeSecon.render("Saisir Date :", True, blackCouleur)
    screen.blit(saisirDate, (colonneGauche.origineX, 30))

    ############Jour ##########
    jour = Button(colonneGauche, posBouttonX=saisirDate.get_rect().width + 5, posBouttonY=30,
                  lBoutton=lMoyenneRale * (2 + 2),
                  hBoutton=tPolice2)
    jour.afficherBoutton(str(datetime.datetime.now().day))

    ############Mois ##############
    mois = Button(colonneGauche, posBouttonX=jour.posX + jour.dim[0] + 5, posBouttonY=30,
                  lBoutton=lMoyenneRale * (2 + 2),
                  hBoutton=tPolice2)
    mois.afficherBoutton(str(datetime.datetime.now().month))

    ############## Annee####################################
    annee = Button(colonneGauche, posBouttonX=mois.posX + mois.dim[0] + 5, posBouttonY=30,
                   lBoutton=lMoyenneRale * (4 + 2),
                   hBoutton=tPolice2)
    annee.afficherBoutton(str(datetime.datetime.now().year))

    ####################################################################################################################

    ############################### Montant ###########################################################################

    ############### Affichage texte######
    saisirMontant = policeSecon.render("Saisir Montant :", True, blackCouleur)
    yTextSaisirMontant = 30 + 1.5 * tPolice2
    screen.blit(saisirMontant, (colonneGauche.origineX, yTextSaisirMontant))
    symbole = policeSecon.render("€", True, blackCouleur)
    screen.blit(symbole, (colonneGauche.origineX, yTextSaisirMontant + tPolice2 + 2))

    ############# Saisi montant ################
    symbRect = symbole.get_rect()
    euro = Button(colonneGauche, posBouttonX=symbRect.x + symbRect.w + 5, posBouttonY=yTextSaisirMontant + tPolice2 + 2,
                  lBoutton=lMoyenneRale * (len("0,00") + 5), hBoutton=tPolice2)
    euro.afficherBoutton(texte="0,00")

    ###################################################################################################################

    ###################### Gestion categorie #########################################################################

    saisirCat = policeSecon.render("Selectionnez la categorie:", True, blackCouleur)
    screen.blit(saisirCat, (colonneGauche.origineX, euro.posY + euro.dim[1] + 30))

    saisirCatRect = saisirCat.get_rect()
    listCat = callCategorie()
    numAffiche = 0

    categorie = Button(colonneGauche, posBouttonX=0,
                       posBouttonY=euro.posY + euro.dim[1] + 30 + saisirCatRect.height + 5,
                       lBoutton=(len(listCat[numAffiche]) + 12) * lMoyenneRale)
    categorie.afficherBoutton(listCat[numAffiche])

    # Max 15 caractere pour une categorie !!!
    catMore = Button(colonneGauche, posBouttonX=(colonneGauche.origineX + (15 + 2) * lMoyenneRale),
                     posBouttonY=categorie.posY,
                     lBoutton=50)
    catMore.afficherBoutton("+")

    catLess = Button(colonneGauche, posBouttonX=catMore.posX + catMore.dim[0] + 5, posBouttonY=catMore.posY,
                     lBoutton=catMore.dim[0])
    catLess.afficherBoutton("-")
    ##################################################################################################################

    #################### Creation de la selection du type de depense ###################################################

    ################ Texte Depense ###############
    textDepense = policeSecon.render("Depense", True, blackCouleur)
    screen.blit(textDepense, (colonneGauche.origineX, categorie.posY + categorie.dim[1] + 30))
    rectTextDepense = textDepense.get_rect()

    ################ Boutton de Selection##########
    typeTrans = Button(colonneGauche, posBouttonX=rectTextDepense[0] + rectTextDepense[2] + 15,
                       posBouttonY=categorie.posY + categorie.dim[1] + 30, lBoutton=80)
    typeTrans.afficherBoutton()

    ############### Etat d origine
    rectSelection = pygame.Rect(typeTrans.posX, typeTrans.posY, 30, typeTrans.dim[1])
    pygame.draw.rect(screen, greenCouleur, rectSelection)
    depense = True

    ###############Texte Benefice ##################
    textBenef = policeSecon.render("Benefice", True, blackCouleur)
    screen.blit(textBenef, (typeTrans.posX + typeTrans.dim[0] + 15, typeTrans.posY))

    #################################################################################################################

    ###################################### Gestion Raison ###########################################################
    raison = Button(colonneGauche, posBouttonX=0, posBouttonY=typeTrans.posY + typeTrans.dim[1] + 45,
                    lBoutton=lMoyenneRale * (30 + 5), hBoutton=tPolice2)
    raison.afficherBoutton(texte="Saisir votre raison")
    ################################################################################################################

    ##################################### Bouton Annuler ###########################################################
    anulerBut = Button(colonneDroite, posBouttonY=colonneDroite.h - 35)
    anulerBut.afficherBoutton(texte="Annuler")
    ################################################################################################################

    ###################################### Boutton de validation ##################################################
    confirmerBut = Button(colonneDroite, anulerBut.posX + anulerBut.dim[0] + 10, posBouttonY=anulerBut.posY)
    confirmerBut.afficherBoutton(texte="Confirmer")
    ##############################################################pygame.Rect(Button.posX + 80 -30, Button.posY, 30, Button.dim[1])##################################################

    pygame.display.update()
    launched = True
    while launched == True:
        for event in pygame.event.get():
            QuitPrgm = event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            if QuitPrgm == True:
                launched = False
                pygame.quit()
                quit()

            if anulerBut.bouttonOn(event):
                Acceuil()

            if typeTrans.bouttonOn(event) == True:
                depense = afficherChoixBoutton(typeTrans, depense)

            if catMore.bouttonOn(event) == True:
                numAffiche = modifCat(True, numAffiche, categorie)

            if catLess.bouttonOn(event) == True:
                numAffiche = modifCat(False, numAffiche, categorie)

            if confirmerBut.bouttonOn(event) == True:
                confirmEnregistrerTrans(numAffiche, annee, mois, jour, euro, raison, depense, listCat)

            if raison.bouttonOn(event) == True:
                raison.afficherBoutton(lMessage=30, entryBox=True, Type=0)

            if jour.bouttonOn(event) == True:
                jour.afficherBoutton(entryBox=True, Type=2, lMessage=2)
                # Ajouter une valeur max pour jour // mois // annee

            if mois.bouttonOn(event) == True:
                mois.afficherBoutton(entryBox=True, Type=2, lMessage=2)

            if annee.bouttonOn(event):
                annee.afficherBoutton(entryBox=True, Type=2, lMessage=4)

            if euro.bouttonOn(event):
                euro.afficherBoutton(entryBox=True, Type=3, lMessage=15)


def Acceuil():
    """
        Cette fonction permet d afficher la fenetre d acceuil !
    """
    pygame.display.set_caption("Acceuil")
    screen.fill(interfaceCouleur)  # On efface l ecran

    # Def des differentes surfaces de l interface.
    colonneDroite = SurfacePerso(screen, lscreen - 420, 0, 200, hscreen)  # On definit la colonne de droite

    salutUtilisateur()  # Afficher du nom de l'utilisateur

    printSolde()  # Afficher Solde

    ################################### Ajouter une transaction ######################################################
    addInter = Button(colonneDroite, posBouttonY=colonneDroite.h - 35)
    addInter.afficherBoutton(texte="Ajouter")

    ###################################################################################################################

    ##################################### Acces aux diagrammes ########################################################
    diagrammeBout = Button(colonneDroite, posBouttonX= addInter.dim[0] + 5, posBouttonY=addInter.posY)
    diagrammeBout.afficherBoutton(texte="Stats")
    ###################################################################################################################

    ################################Afficher les dernieres transactions ###############################################
    hauteur = hscreen / 4

    derniereTransText = policePrin.render("Dernieres Transactions Saisies:", True, blackCouleur)
    screen.blit(derniereTransText, (30, hauteur - 80))

    moisJ = datetime.datetime.now().month
    anneeJ = datetime.datetime.now().year
    transactionMois = recupTransaction(moisJ, anneeJ)

    while transactionMois == False:
        if moisJ - 1 == 0:
            moisJ = 12
            anneeJ -= 1
        else:
            moisJ -= 1
        # Si on n a pas de transaction ce mois ci on ira prendre celle du mois precedent
        if anneeJ == 2018:
            # On ne permet pas d entreer des transactions avant 2019.
            # On affichera donc " aucune transaction "
            transactionMois = True
        if transactionMois != True:
            transactionMois = recupTransaction(moisJ, anneeJ)

    if transactionMois != []:
        for k in range(0, len(transactionMois)):
            compteur = len(transactionMois) - 1 - k  # On affiche les dernieres transactions en haut

            if transactionMois[compteur].type == True and hauteur + tPolice2 < addInter.posY:
                texteTrans = str(transactionMois[compteur].date) + "        " + "-" + str(
                    transactionMois[compteur].montant) + "€" + "        " + str(transactionMois[compteur].raison)
                transaction = policeSecon.render(texteTrans, True, redCouleur)
                screen.blit(transaction, (0, hauteur))
                rectTransaction = transaction.get_rect()
                pygame.draw.line(screen, blackCouleur, (0, hauteur + tPolice2),
                                 (rectTransaction.w, hauteur + tPolice2), 2)
                hauteur += tPolice2 + 5
                # Oblige de mettre 2 fois a colle sur l ecran car sinon on reecrira la transaction precedente
            elif hauteur + tPolice2 < addInter.posY:
                texteTrans = str(transactionMois[compteur].date) + "        " + str(
                    transactionMois[compteur].montant) + "€" + "        " + str(transactionMois[compteur].raison)
                transaction = policeSecon.render(texteTrans, True, greenCouleur)
                screen.blit(transaction, (0, hauteur))
                rectTransaction = transaction.get_rect()
                pygame.draw.line(screen, blackCouleur, (0, hauteur + tPolice2),
                                 (rectTransaction.w, hauteur + tPolice2), 2)
                hauteur += tPolice2 + 5
    else:
        # Si aucune transaction n est detecte, on affiche simplement aucune transac
        transaction = policeMiseAv.render("-- Aucune Transaction Recente--", True, blackCouleur)
        rectTransaction = transaction.get_rect()
        screen.blit(transaction, (lscreen / 2 - rectTransaction.w / 2, 2 * hauteur))

    ###################################################################################################################

    pygame.display.update()
    launched = True
    while launched == True:
        for event in pygame.event.get():
            QuitPrgm = event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE

            if QuitPrgm == True:
                launched = False
                pygame.quit()
                quit()

            if addInter.bouttonOn(event) == True:
                addT()

            if diagrammeBout.bouttonOn(event) == True:
                diagramme()


def Inscription():
    pygame.display.set_caption("Inscription")
    screen.fill(interfaceCouleur)

    colonneCentral = SurfacePerso(screen, lscreen / 2 - lMoyenneRale * 10, hscreen / 4, lMoyenneRale * 20, hscreen)

    ########################################## NOM - Prenom ############################################################
    boxPrenom = Button(colonneCentral, 0, 0)
    boxPrenom.afficherBoutton("Entrez Prenom")

    boxNom = Button(colonneCentral, 0, boxPrenom.posY + boxPrenom.dim[1] + 10)
    boxNom.afficherBoutton("Entrez Nom")
    ###################################################################################################################

    ######################################### SOLDE ###################################################################
    boxSolde = Button(colonneCentral, 0, boxNom.posY + boxNom.dim[1] + 10)
    boxSolde.afficherBoutton("Entrez Solde")
    ###################################################################################################################

    ###################################Instructions####################################################################
    afficherInstructions(boxSolde)
    ###################################################################################################################

    ########################################### Confirmer #############################################################
    confimer = Button(colonneCentral, 0, hscreen - 250)
    confimer.afficherBoutton("Confirmer")
    ###################################################################################################################
    pygame.display.update()
    launched = True
    while launched == True:
        for event in pygame.event.get():
            QuitPrgm = event.type == pygame.QUIT

            if QuitPrgm == True:
                launched = False
                pygame.quit()
                quit()

            if boxPrenom.bouttonOn(event):
                boxPrenom.afficherBoutton(lMessage=10, entryBox=True, Type=0)

            if boxNom.bouttonOn(event):
                boxNom.afficherBoutton(lMessage=10, entryBox=True, Type=0)

            if boxSolde.bouttonOn(event):
                boxSolde.afficherBoutton(entryBox=True, Type=3)

            if confimer.bouttonOn(event):
                nouvelUser(boxNom, boxPrenom, boxSolde)
                Acceuil()


#####################################PROGRAMME PRINCIPAL#######################################################
pygame.init()
pygame.font.init()
policePrin = pygame.font.SysFont('ressources/fonts/latto.ttf', tPolice)  # Police Principal
policeSecon = pygame.font.SysFont('ressources/fonts/raleway.tff', tPolice2)
policeMiseAv = pygame.font.SysFont('ressources/fonts/raleway.tff', tMiseAv)
# Creation fenetre pygame :
screen = pygame.display.set_mode((lscreen, hscreen))
# Couleur interface
interfaceCouleur = setCouleurInterface()

if os.path.exists("ressources/user") == False:
    Inscription()
else:
    Acceuil()
#####################################FIN PROGRAMME PRINCIPAL####################################################
