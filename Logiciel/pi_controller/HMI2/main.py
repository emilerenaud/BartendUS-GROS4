import sys
import time
# from calib import Calibration_cam
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets as qtw
from PyQt5.QtWidgets import QDialog, QApplication, QInputDialog, QListWidgetItem, QPushButton, QMessageBox
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from librairieRecette import livreRecette,ingredient_dispo,recette
from stateMachine import communication


#init des variables globales
livreRecette=livreRecette()
livreIngredient=ingredient_dispo()
max_Bouteille=9


# Step 1: Create a worker class
class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(object)

    def run(self):
        """state_machine"""

        self.finished.emit()


class MainWindow(QDialog):
    def __init__(self):
        print("refresh")
        super(MainWindow, self).__init__()
        loadUi("MainWindowDialog.ui", self)
        self.recettes.clicked.connect(self.go_to_recettes)
        self.boire.clicked.connect(self.go_to_boire)
        self.boire.clicked.connect(self.show_popup)
        self.bouteilles.clicked.connect(self.go_to_bouteilles)
        self.reglages.clicked.connect(self.go_to_reglages)

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

    def go_to_reglages(self):
        screen5 = reglages_screen5()
        widget.addWidget(screen5)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def show_popup(self):
        print('allo')
        msg = qtw.QMessageBox()
        msg.setWindowTitle("BartendUS")
        msg.setText("Assurez-vous de mettre un verre avant de commander")
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.buttonClicked.connect(self.popup_button)
        x = msg.exec_()

    def popup_button(self):
        # buttonClicked appeler Fonction Tony
        print('bouton connect')




#*****************************************************************************************************WINDOW RECETTE
class recette_screen2(QDialog):
    def __init__(self):
        super(recette_screen2, self).__init__()
        loadUi("recette.ui", self)
        print("refresh")
        # mettre les recettes a jour dans la liste widget sans bouton
        self.precedent.clicked.connect(self.go_to_MainWindowDialog)
        self.ajouter_alcool.clicked.connect(self.ajouter_ingredient)
        self.ajouter_recette.clicked.connect(self.ajouter_livreRecette)
        self.supprimer.clicked.connect(self.supprimer_ligne)
        self.delete_all.clicked.connect(self.supprimer_tout)
        self.liste_ingredient_recette=[]
        self.liste_quantite_recette=[]
        # self.listWidget.itemDoubleClicked.connect(self.dispSelected)

    def go_to_MainWindowDialog(self):
        mainwindow=MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def ajouter_ingredient(self):
        # travailler l'affichage de la liste widget

        alcool = self.alcool_ligne.text()
        quantite = self.quantite_ligne.text()

        if alcool == "":
            qtw.QMessageBox.information(self, 'Attention', '''Aucun alcool entrée'''+ "\n" + '''Réessayer...''')
            return
        try:
            quantite=float(quantite)
        except:
            qtw.QMessageBox.information(self, 'Erreur',
                                        '''La quantité "''' + quantite + '''" n'est pas un chiffre.''' + "\n" + '''Réessayer...''')
            return

        if quantite > 8:
            qtw.QMessageBox.information(self, 'Attention', '''La quantité d'alcool est supérieure à 8 oz'''+ "\n" + '''Réessayer...''')
            return

        self.liste_ingredient_recette.append(alcool)
        self.liste_quantite_recette.append(quantite)

        chaine_temp = alcool + ': ' + str(quantite) + 'oz'
        self.listWidget.addItem(chaine_temp)

        self.alcool_ligne.setText('')
        self.alcool_ligne.setFocus()
        self.titre_ligne.setText('')
        self.titre_ligne.setFocus()
        self.quantite_ligne.setText('')
        self.quantite_ligne.setFocus()



    def supprimer_ligne(self):
        row=self.listWidget.currentRow()
        if(row>=0):
            print(row)
            self.listWidget.takeItem(row)
            self.liste_ingredient_recette.pop(row)
            self.liste_quantite_recette.pop(row)


    def supprimer_tout(self):
        self.listWidget.clear()
        self.liste_ingredient_recette.clear()
        self.liste_quantite_recette.clear()

    def ajouter_livreRecette(self):

        titre = self.titre_ligne.text()
        if titre == "":
            qtw.QMessageBox.information(self, 'Erreur','''Aucun titre''' + "\n" + '''Réessayer...''')
            return

        livreRecette.ajouterRecette(titre,self.liste_ingredient_recette,self.liste_quantite_recette)
        livreRecette.update_recette_dispo(livreIngredient)
        self.liste_ingredient_recette.clear()
        self.liste_quantite_recette.clear()
        self.listWidget.clear()
        #clear le texte des boites
        self.alcool_ligne.setText('')
        self.alcool_ligne.setFocus()
        self.titre_ligne.setText('')
        self.titre_ligne.setFocus()
        self.quantite_ligne.setText('')
        self.quantite_ligne.setFocus()




#***********************************************************************************************WINDOW BOIRE
class boire_screen3(QDialog):
    def __init__(self):
        super(boire_screen3, self).__init__()
        loadUi("Boire.ui", self)
        #mise a jour recette_dispo
        livreRecette.update_recette_dispo(livreIngredient)

        if(len(livreRecette.list_recette_dispo_string())>0):
            self.recettes_disponibles.addItems(livreRecette.list_recette_dispo_string())
        else:
            self.recettes_disponibles.addItem("Aucune Recette Compatible")


        self.recettes_disponibles.itemClicked.connect(self.voir_liste_ingredient)
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

    def voir_liste_ingredient(self):
        self.ingredients.clear()
        # afficher la liste d'ingrédients avec l'indice de la liste des recettes disponibles
        row = self.recettes_disponibles.currentRow()
        self.ingredients.addItem(livreRecette.list_recette_dispo[row].afficherIngredient())

    def commander_verre(self):

        # verif_seuil = Calibration_cam()
        # if not verif_seuil.calib_vision_seuil():
        #     qtw.QMessageBox.critical(self, 'Fail', '''La caméra doit être calibrée.''')
        #     reglages_screen5.calibration(self)
        #     return

        # row = self.recettes_disponibles.currentRow()
        # recette_commander=livreRecette.list_recette_dispo[row]

        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        #self.worker.progress.connect(self.afficherTest)
        # Step 6: Start the thread
        self.thread.start()

        # self.thread.finished.connect(
        #     lambda: self.commander.setEnabled(False)
        # )



    def radioBouton(self):
        self.type_boire = 0
        if self.radioVerre.isChecked() == True:
            self.type_boire = 1
        if self.radioShot.isChecked() == True:
            self.type_boire = 2




#***********************************************************************************************WINDOW BOUTEILLE
class bouteilles_screen4(QDialog):
    def __init__(self):
        super(bouteilles_screen4, self).__init__()
        loadUi("bouteilles.ui", self)

        # Initialisation des listes ici afin d'afficher des le debut ## additems(getlistingredients.text())
        self.quantite_ingredient=0
        self.precedent.clicked.connect(self.go_to_MainWindowDialog)
        self.ajouter.clicked.connect(self.ajouter_ingredient)
        self.supprimer.clicked.connect(self.supprimer_ligne)

        # self.label.setScaledContents(True)
        # self.label.setPixmap(QPixmap("icône-ou-logo-de-la-meilleure-qualité-d-alcool-dans-ligne-style-102955105.jpeg"))

        self.niveau_alcool.valueChanged.connect(self.slidervertical)
        self.update_liste()
    def slidervertical(self, value):
        self.quantite_ingredient = value

    def go_to_MainWindowDialog(self):
        mainwindow=MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def ajouter_ingredient(self):

        ingredient = self.ingredient_ligne.text()
        position_ingredient = self.position_ingredient_ligne.text()

        if position_ingredient.isdigit()  :
            position_ingredient = int(position_ingredient)
        else:
            qtw.QMessageBox.information(self, 'Erreur position', '''La position"'''+position_ingredient+'''" est invalide.''')
            return

        if position_ingredient > max_Bouteille:
            qtw.QMessageBox.information(self, 'Erreur position', '''La position est trop élevé\n'''+'''Les positions valides sont de 0 à '''+str(max_Bouteille))
            return

        try:
             print(livreIngredient.list_position)
             livreIngredient.list_position.index(position_ingredient)
             qtw.QMessageBox.information(self, 'Erreur Doublon', '''La  position : "''' + str(position_ingredient) + '''" est déjà occuper par une bouteille''')
             return
        except:
            pass

        try:
            livreIngredient.list_ingredient.index(ingredient)
            qtw.QMessageBox.information(self, 'Erreur Doublon','''L'ingrédient : "''' + ingredient + '''" est déjà présent dans la liste''')
            return
        except:
            pass


        livreIngredient.ajouterIngredient(ingredient,self.quantite_ingredient,position_ingredient)

        self.ingredient_ligne.setText('')
        self.ingredient_ligne.setFocus()
        self.position_ingredient_ligne.setText('')
        self.position_ingredient_ligne.setFocus()
        self.update_liste()

    def supprimer_ligne(self):
        # avec currenrow qui donne l'indice appeler supprimerIngredient
        #faire un update donc call update_liste
        row=self.liste_bouteilles.currentRow()
        if row>=0:
            self.liste_bouteilles.takeItem(row)
            livreIngredient.supprimerIngredient(row)
            self.update_liste()

    def update_liste(self):
        # clear la liste liste_bouteilles
        # addItems
        self.liste_bouteilles.clear()
        self.liste_bouteilles.addItems(livreIngredient.get_list_ingredient_string())
        return

class reglages_screen5(QDialog):
    def __init__(self):
        super(reglages_screen5, self).__init__()

        loadUi("Reglage_v2.ui", self)

        self.precedent.clicked.connect(self.go_to_MainWindowDialog)
        self.home_x.clicked.connect(self.HOME_X)
        self.home_y.clicked.connect(self.HOME_Y)
        self.home_z.clicked.connect(self.HOME_Z)
        self.home_all.clicked.connect(self.HOME_ALL)
        self.bouton_electroaimant.clicked.connect(self.activer_electroaimant)
        self.bouton_calibration.clicked.connect(self.calibration)
        self.go_to.clicked.connect(self.go_to_position)
        self.o_servo.clicked.connect(self.ouverture_servo)
        self.f_servo.clicked.connect(self.fermeture_servo)

    def go_to_MainWindowDialog(self):
        mainwindow=MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def HOME_X(self):
        print('aller home x')

    def HOME_Y(self):
        print('aller home y')

    def HOME_Z(self):
        print('aller home z')

    def HOME_ALL(self):
        print('aller home all')

    def activer_electroaimant(self):
        print('activer_electroaimant')

    def calibration(self):
        # calib = Calibration_cam()
        print('activer calibration')

    def go_to_position(self):
        print('aller à la position')

    def ouverture_servo(self):
        print('ouverture servo')

    def fermeture_servo(self):
        print('fermeture servo')


app = QApplication(sys.argv)
widget=qtw.QStackedWidget()


mainwindow=MainWindow()
widget.addWidget(mainwindow)
widget.setFixedHeight(720)
widget.setFixedWidth(1280)
widget.show()
#widget.showFullScreen()

try:
    sys.exit(app.exec_())

except:
    print("Exiting")

