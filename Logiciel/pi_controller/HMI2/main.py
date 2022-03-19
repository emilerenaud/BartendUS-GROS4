import sys
from PyQt5.uic import loadUi
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PyQt5 import QtWidgets as qtw
from PyQt5.QtWidgets import QDialog, QApplication, QInputDialog, QListWidgetItem, QPushButton

# Variable globale pour ajouter recette
liste_alcool_recette = []
titre_recette = ''
liste_quantite_recette = []
option = 0

# Variable globale pour ajouter bouteille
liste_bouteille_ingredient = []
liste_quantite_ingredient = []
liste_position_ingredient = []
quantite_ingredient = 0

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("MainWindowDialog.ui", self)
        self.recettes.clicked.connect(self.go_to_recettes)
        self.boire.clicked.connect(self.go_to_boire)
        self.bouteilles.clicked.connect(self.go_to_bouteilles)



        # self.container = QFrame()
        # self.container.setObjectName("container")
        # self.container.setStyleSheet("#container { background-color: #222 }")
        # self.layout = QVBoxLayout()
        #
        # # ADD WIDGETS TO LAYOUT
        # self.toggle = QPushButton("Teste")
        # # layout pt haut
        # self.layout.addWidget(self.toggle, Qt.AlignCenter, QtAlignCenter)
        # self.container.setLayout(self.layout)
        # self.setCentralWidget(self.container)


    def go_to_recettes(self):
        screen2 = recette_screen2()
        widget.addWidget(screen2)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def go_to_boire(self):
        screen3 = boire_screen3()
        widget.addWidget(screen3)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def go_to_bouteilles(self):
        screen4 = bouteilles_screen4()
        widget.addWidget(screen4)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class recette_screen2(QDialog):
    def __init__(self):
        super(recette_screen2, self).__init__()
        loadUi("recette.ui", self)

        # mettre les recettes a jour dans la liste widget sans bouton
        self.precedent.clicked.connect(self.go_to_MainWindowDialog)
        self.ajouter_alcool.clicked.connect(self.ajouter_liste)
        self.ajouter_recette.clicked.connect(self.ajouter_livre_recette)
        self.supprimer.clicked.connect(self.supprimer_ligne)
        self.delete_all.clicked.connect(self.supprimer_tout)
        self.edit.clicked.connect(self.editlist)

        # self.listWidget.itemDoubleClicked.connect(self.dispSelected)

    def go_to_MainWindowDialog(self):
        mainwindow=MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def ajouter_liste(self):
        # travailler l'affichage de la liste widget

        alcool = self.alcool_ligne.text()
        titre = self.titre_ligne.text()
        quantite = self.quantite_ligne.text()

        if quantite.isdigit():
            quantite_verif = int(quantite)
        else:
            qtw.QMessageBox.information(self, 'Fail', '''La quantité n'est pas un chiffre.''')
        print(quantite_verif)
        if quantite_verif > 8:
            qtw.QMessageBox.information(self, 'Fail', '''La quantité d'alcool est supérieure à 8 oz''')

        liste_alcool_recette.append(alcool)
        liste_quantite_bouteille.append(quantite)

        chaine_temp = self.alcool_ligne.text() + '(' + self.quantite_ligne.text() + 'oz)'
        self.listWidget.addItem(chaine_temp)

        self.alcool_ligne.setText('')
        self.alcool_ligne.setFocus()
        self.titre_ligne.setText('')
        self.titre_ligne.setFocus()
        self.quantite_ligne.setText('')
        self.quantite_ligne.setFocus()

    def editlist(self):
        row = self.listWidget.currentRow()
        newtext, ok = QInputDialog.getText(self, "Enter new text", "Enter new text")
        if ok and (len(newtext) != 0):
            self.listWidget.takeItem(self.listWidget.currentRow())
            self.listWidget.insertItem(row, QListWidgetItem(newtext))

    def supprimer_ligne(self):
        self.listWidget.takeItem(self.listWidget.currentRow())
    def supprimer_tout(self):
        self.listWidget.clear()

    def ajouter_livre_recette(self):
        # APPELLE DE LA FONCTION A TONY AVEC LISTE_ALCOOL_RECETTE, LISTE_LISTE_QUANTITE_RECETTE, TITRE_RECETTE
        print('la recette a ete ajoute')

class boire_screen3(QDialog):
    def __init__(self):
        super(boire_screen3, self).__init__()
        loadUi("Boire.ui", self)

        # afficher la liste de recette disponible
        self.recettes_disponibles.addItem('chaine_temp1')
        # afficher la liste des ingrédients de la premiere recette sélectionnée (initialisation)

        self.ingredients.addItem('ingredients de la premiere recette')
        # mettre a jour ajouter ingredients a chaque fois qu'on selectionne element de la liste recette
        self.recettes_disponibles.itemClicked.connect(self.ajouter_ingredient_liste)

        self.precedent.clicked.connect(self.go_to_MainWindowDialog)
        self.commander.clicked.connect(self.commander_verre)
        self.radioVerre.setChecked(True)
        self.radioVerre.toggled.connect(self.radioBouton)
        self.radioShot.toggled.connect(self.radioBouton)
        # mettre les recettes a jour dans la liste widget sans bouton


    def go_to_MainWindowDialog(self):
        mainwindow=MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def ajouter_ingredient_liste(self):
        # afficher la liste d'ingrédients avec l'indice de la liste des recettes disponibles
        row = self.recettes_disponibles.currentRow()
        print(row)
        self.ingredients.addItem('ingrédients')

    def commander_verre(self):
        print('commander')

    def radioBouton(self):
        self.type_boire = 0
        if self.radioVerre.isChecked() == True:
            self.type_boire = 1
        if self.radioShot.isChecked() == True:
            self.type_boire = 2

class bouteilles_screen4(QDialog):
    def __init__(self):
        super(bouteilles_screen4, self).__init__()
        loadUi("bouteilles.ui", self)

        # Initialisation des listes ici afin d'afficher des le debut ## additems(getlistingredients.text())

        self.precedent.clicked.connect(self.go_to_MainWindowDialog)
        self.ajouter.clicked.connect(self.ajouter_ingredient)
        self.supprimer.clicked.connect(self.supprimer_ligne)

        # self.label.setScaledContents(True)
        # self.label.setPixmap(QPixmap("icône-ou-logo-de-la-meilleure-qualité-d-alcool-dans-ligne-style-102955105.jpeg"))

        self.niveau_alcool.valueChanged.connect(self.slidervertical)

    def slidervertical(self, value):
        quantite_ingredient = str(value)

    def go_to_MainWindowDialog(self):
        mainwindow=MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def ajouter_ingredient(self):
        # regarder avec tony quel fonction mettre pas certain probablment un setingredientlist
        ingredient = self.ingredient_ligne.text()
        position_ingredient = self.position_ingredient_ligne.text()

        if position_ingredient.isdigit():
            position_verif_ingredient = int(position_ingredient)
        else:
            qtw.QMessageBox.information(self, 'Fail', '''La position n'est pas un chiffre.''')

        if position_verif_ingredient > 8:
            qtw.QMessageBox.information(self, 'Fail', '''La position que vous avez donné n'existe pas.''')

        liste_bouteille_ingredient.append(ingredient)
        liste_position_ingredient.append(position_verif_ingredient)
        liste_quantite_ingredient.append(quantite_ingredient)

        ingredient = self.ingredient_ligne.text()
        position_ingredient = self.position_ingredient_ligne.text()

        chaine_temp1 = 'Ingrédient : ' + self.ingredient_ligne.text() + ' - Position : ' + self.position_ingredient_ligne.text()
        chaine_temp2 = 'Ingrédient2 : ' + self.ingredient_ligne.text() + ' - Position : ' + self.position_ingredient_ligne.text()
        liste_chaine=[chaine_temp1,chaine_temp2]
        self.liste_bouteilles.addItems(liste_chaine)

        self.ingredient_ligne.setText('')
        self.ingredient_ligne.setFocus()

        self.position_ingredient_ligne.setText('')
        self.position_ingredient_ligne.setFocus()

    def supprimer_ligne(self):
        # avec currenrow qui donne l'indice appeler supprimerIngredient
        #faire un update donc call update_liste

        #self.liste_bouteilles.takeItem(self.liste_bouteilles.currentRow())

    def update_liste(self):
        # clear la liste liste_bouteilles
        # addItems



app = QApplication(sys.argv)
widget=qtw.QStackedWidget()

#init
#livreRecette=livreRecette()

#creer recette
# livreRecette.ajouterRecette
# livreRecette.liste_recette_dispo[index].afficherIngredient

mainwindow=MainWindow()
widget.addWidget(mainwindow)
widget.setFixedHeight(500)
widget.setFixedWidth(500)
widget.show()



try:
    sys.exit(app.exec_())
except:
    print("Exiting")