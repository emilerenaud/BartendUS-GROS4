import sys
import time
#from calibration import Calibration_cam
from Vision.calibration import Calibration_cam
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets as qtw
from PyQt5.QtWidgets import QDialog, QApplication, QInputDialog, QListWidgetItem, QPushButton, QMessageBox
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from pi_controller.HMI2.librairieRecette import gestion_Recette,gestion_ingredient_dispo,recette
from stateMachine import sequence


#init des variables globales
livreRecette=gestion_Recette()
livreIngredient=gestion_ingredient_dispo()
#calib = Calibration_cam()
max_Bouteille=9
#sequence=sequence()


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
        loadUi("pi_controller/HMI2/MainWindowDialog.ui", self)
        self.recettes.clicked.connect(self.go_to_recettes)
        self.boire.clicked.connect(self.go_to_boire)
        # self.boire.clicked.connect(self.show_popup)
        self.bouteilles.clicked.connect(self.go_to_bouteilles)
        self.consulter.clicked.connect(self.go_to_consulter_recettes)
        self.reglages.clicked.connect(self.go_to_reglages)



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

    def go_to_consulter_recettes(self):
        screen7 = consulter_recettes_screen7()
        widget.addWidget(screen7)
        widget.setCurrentIndex(widget.currentIndex() + 1)


#*****************************************************************************************************WINDOW RECETTE
class recette_screen2(QDialog):
    def __init__(self):
        super(recette_screen2, self).__init__()
        loadUi("pi_controller/HMI2/recette.ui", self)
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
        loadUi("pi_controller/HMI2/Boire.ui", self)
        #mise a jour recette_dispo
        livreRecette.update_recette_dispo(livreIngredient)

        if(len(livreRecette.list_recette_dispo_string())>0):
            self.recettes_disponibles.addItems(livreRecette.list_recette_dispo_string())
        else:
            self.recettes_disponibles.addItem("Aucune Recette Compatible")


        self.recettes_disponibles.itemClicked.connect(self.voir_liste_ingredient)
        self.precedent.clicked.connect(self.go_to_MainWindowDialog)
        self.commander.clicked.connect(self.commander_screen6)



    def go_to_MainWindowDialog(self):
        mainwindow=MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def voir_liste_ingredient(self):
        # afficher la liste d'ingrédients avec l'indice de la liste des recettes disponibles
        row = self.recettes_disponibles.currentRow()
        if row>=0 and len(livreRecette.list_recette_dispo_string())>0:
            self.ingredients.clear()
            self.ingredients.addItem(livreRecette.list_recette_dispo[row].afficherIngredient())

    def commander_screen6(self):
        row = self.recettes_disponibles.currentRow()
        recette_commander = livreRecette.list_recette_dispo[row]
        screen6 = commander_screen6(recette_commander)
        widget.addWidget(screen6)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class commander_screen6(QDialog):
    def __init__(self, recette):
        super(commander_screen6, self).__init__()

        loadUi("pi_controller/HMI2/commander.ui", self)

        self.annuler.clicked.connect(self.go_to_Boire)
        self.terminer.clicked.connect(self.go_to_MainWindowDialog)
        self.terminer.clicked.connect(self.commander_verre)
        self.incrementer.clicked.connect(self.incrementer_compteur_verre)
        self.decrementer.clicked.connect(self.decrementer_compteur_verre)
        self.incrementer.clicked.connect(self.afficher_compteur)
        self.decrementer.clicked.connect(self.afficher_compteur)
        self.recette = recette
        self.nb_verre = 0
        self.nombre_verre.setText('''Nombre de verre : "''' + str(self.nb_verre) + '''"''')

    def go_to_Boire(self):
        windowBoire=boire_screen3()
        widget.addWidget(windowBoire)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def go_to_MainWindowDialog(self):
        mainwindow=MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def incrementer_compteur_verre(self):
        if self.nb_verre < 8:
            self.nb_verre = self.nb_verre + 1
        else:
            qtw.QMessageBox.critical(self, 'Fail', '''Le nombre de verre ne peut pas avoir une valeur plus grande que 8.''')

    def decrementer_compteur_verre(self):
        if self.nb_verre > 0:
            self.nb_verre = self.nb_verre - 1
        else:
            qtw.QMessageBox.critical(self, 'Fail', '''Le nombre de verre ne peut pas avoir une valeur négative''')

    def afficher_compteur(self):
        str_nb_verre = str(self.nb_verre)
        self.nombre_verre.setText('''Nombre de verre : "''' + str_nb_verre + '''"''')


    def commander_verre(self):
           # print("pompe activer : ",sequence.pompe(recette_commander,livreIngredient))

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




#***********************************************************************************************WINDOW BOUTEILLE
class bouteilles_screen4(QDialog):
    def __init__(self):
        super(bouteilles_screen4, self).__init__()
        loadUi("pi_controller/HMI2/bouteilles.ui", self)

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
        self.quantite_ingredient = value*750/100

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

class consulter_recettes_screen7(QDialog):
    def __init__(self):
        super(consulter_recettes_screen7, self).__init__()
        loadUi("pi_controller/HMI2/consulter_recette.ui", self)

        self.precedent.clicked.connect(self.go_to_MainWindowDialog)
        self.supprimer.clicked.connect(self.supprimer_recette)

    def go_to_MainWindowDialog(self):
        mainwindow=MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def supprimer_recette(self):
        pass

class reglages_screen5(QDialog):
    def __init__(self):
        super(reglages_screen5, self).__init__()
        loadUi("pi_controller/HMI2/Reglage_v2.ui", self)

        self.precedent.clicked.connect(self.go_to_MainWindowDialog)
        self.home_all.clicked.connect(self.HOME_ALL)
        self.bouton_calibration.clicked.connect(self.calibration)
        self.move_to.clicked.connect(self.go_to_position)
        self.bouton_electro.clicked.connect(self.radioBouton_electro)
        self.bouton_servo.clicked.connect(self.radioBouton_servo)

        self.radio_ouverture_servo.setChecked(True)
        self.radio_ouverture_electro.setChecked(True)

    def go_to_MainWindowDialog(self):
        mainwindow=MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def HOME_ALL(self):
        print('aller home all')

    def calibration(self):
        #calib.calib_vision_init()
        print('activer calibration')

    def go_to_position(self):
        print('aller à la position')

    def radioBouton_servo(self):
        self.type_servo = 0
        if self.radio_ouverture_servo.isChecked() == True:
            self.type_servo = 0
        if self.radio_fermeture_servo.isChecked() == True:
            self.type_servo = 1

    def radioBouton_electro(self):
        self.type_electro = 0
        if self.radio_ouverture_electro.isChecked() == True:
            self.type_electro = 0
        if self.radio_fermeture_electro.isChecked() == True:
            self.type_electro = 1

    def commande_purge_pompes(self):
        print('purge')


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

