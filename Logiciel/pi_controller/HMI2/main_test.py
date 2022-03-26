import sys
import time
#from calibration import Calibration_cam
from Logiciel.Vision.calibration import Calibration_cam
# from Logiciel.Vision.calibration import Calibration_cam
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets as qtw
from PyQt5.QtWidgets import QDialog, QApplication, QInputDialog, QListWidgetItem, QPushButton, QMessageBox
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from Logiciel.pi_controller.HMI2.librairieRecette import gestion_Recette,gestion_ingredient_dispo,recette
from pi_controller.HMI2.librairieRecette import gestion_Recette,gestion_ingredient_dispo,recette
from stateMachine import sequence



#init des variables globales
livreRecette=gestion_Recette()
livreIngredient=gestion_ingredient_dispo()

        loadUi("pi_controller/HMI2/MainWindowDialog.ui", self)
        self.recettes.clicked.connect(self.go_to_recettes)
        self.boire.clicked.connect(self.go_to_boire)
        self.boire.clicked.connect(self.show_popup)
        # self.boire.clicked.connect(self.show_popup)
        self.bouteilles.clicked.connect(self.go_to_bouteilles)
        self.consulter.clicked.connect(self.go_to_consulter_recettes)
        self.reglages.clicked.connect(self.go_to_reglages)


        # self.container = QFrame()
        # self.container.setObjectName("container")
        # self.container.setStyleSheet("#container { background-color: #222 }")

        screen4 = bouteilles_screen4()
        widget.addWidget(screen4)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_to_consulter_recettes(self):
        screen7 = consulter_recettes_screen7()
        widget.addWidget(screen7)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_to_reglages(self):
        screen5 = reglages_screen5()
        widget.addWidget(screen5)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def show_popup(self):
        msg = qtw.QMessageBox()
        msg.setWindowTitle("BartendUS")
        msg.setText("Assurez-vous de mettre un verre avant de commander")
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.buttonClicked.connect(self.popup_button)
        x = msg.exec_()
    # def show_popup(self):
    #     msg = qtw.QMessageBox()
    #     msg.setWindowTitle("BartendUS")
    #     msg.setText("Assurez-vous de mettre un verre avant de commander")
    #     msg.setIcon(QMessageBox.Question)
    #     msg.setStandardButtons(QMessageBox.Ok)
    #     msg.buttonClicked.connect(self.popup_button)
    #     x = msg.exec_()

    def popup_button(self):
        # buttonClicked appeler Fonction Tony

        self.delete_all.clicked.connect(self.supprimer_tout)
        self.liste_ingredient_recette=[]
        self.liste_quantite_recette=[]
        # self.listWidget.itemDoubleClicked.connect(self.dispSelected)

    def go_to_MainWindowDialog(self):
        mainwindow=MainWindow()

        self.quantite_ligne.setText('')
        self.quantite_ligne.setFocus()



    def supprimer_ligne(self):
        row=self.listWidget.currentRow()
        if(row>=0):

            self.liste_ingredient_recette.pop(row)
            self.liste_quantite_recette.pop(row)


    def supprimer_tout(self):
        self.listWidget.clear()
        self.liste_ingredient_recette.clear()


        self.recettes_disponibles.itemClicked.connect(self.voir_liste_ingredient)
        self.precedent.clicked.connect(self.go_to_MainWindowDialog)
        self.commander.clicked.connect(self.commander_verre)
        self.radioVerre.setChecked(True)
        self.radioVerre.toggled.connect(self.radioBouton)
        self.radioShot.toggled.connect(self.radioBouton)
        self.commander.clicked.connect(self.go_to_commander_screen6)

        # mettre les recettes a jour dans la liste widget sans bouton

        print(self.recettes_disponibles.currentRow())


    def go_to_MainWindowDialog(self):
        mainwindow=MainWindow()

            self.ingredients.clear()
            self.ingredients.addItem(livreRecette.list_recette_dispo[row].afficherIngredient())



    def commander_verre(self):
    def go_to_commander_screen6(self):
        # print(self.recettes_disponibles.currentRow())
        # print(self.recettes_disponibles.currentItem().text())
        row = self.recettes_disponibles.currentRow()

        # if row == 0:
        #     print('allo4')
        #     self.recettes_disponibles.itemActivated(self.recettes_disponibles.item(0))
        #     print('active')

        if row >= 0 and len(livreRecette.list_recette_dispo_string()) > 0:
            recette_commander=livreRecette.list_recette_dispo[row]
           # print("pompe activer : ",sequence.pompe(recette_commander,livreIngredient))
        # verif_seuil = Calibration_cam()
        # if not verif_seuil.calib_vision_seuil():
        #     qtw.QMessageBox.critical(self, 'Fail', '''La caméra doit être calibrée.''')
        #     reglages_screen5.calibration(self)
        #     return

        # row = self.recettes_disponibles.currentRow()
        # recette_commander=livreRecette.list_recette_dispo[row]
            recette_commander = livreRecette.list_recette_dispo[row]
            screen6=commander_screen6(recette_commander)
            widget.addWidget(screen6)
            widget.setCurrentIndex(widget.currentIndex()+1)
        else:
            return

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
    # def radioBouton(self):
    #     self.type_boire = 0
    #     if self.radioVerre.isChecked() == True:
    #         self.type_boire = 1
    #     if self.radioShot.isChecked() == True:
    #         self.type_boire = 2





        self.niveau_alcool.valueChanged.connect(self.slidervertical)
        self.update_liste()

    def slidervertical(self, value):
        self.quantite_ingredient = value*750/100


        self.liste_bouteilles.addItems(livreIngredient.get_list_ingredient_string())
        return

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
        self.home_x.clicked.connect(self.HOME_X)
        self.home_y.clicked.connect(self.HOME_Y)
        self.home_z.clicked.connect(self.HOME_Z)
        self.home_all.clicked.connect(self.HOME_ALL)
        self.bouton_electroaimant.clicked.connect(self.activer_electroaimant)
        self.bouton_electro.clicked.connect(self.radioBouton_electro)
        self.bouton_servo.clicked.connect(self.radioBouton_servo)

        self.bouton_calibration.clicked.connect(self.calibration)
        self.go_to.clicked.connect(self.go_to_position)
        self.o_servo.clicked.connect(self.ouverture_servo)
        self.f_servo.clicked.connect(self.fermeture_servo)
        self.move_to.clicked.connect(self.go_to_position)

        self.radio_ouverture_servo.setChecked(True)
        self.radio_ouverture_electro.setChecked(True)

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
        #calib.calib_vision_init()
        print('activer calibration')

    def go_to_position(self):
        print('aller à la position')

    def ouverture_servo(self):
        print('ouverture servo')
    def radioBouton_servo(self):
        self.type_servo = 0
        if self.radio_ouverture_servo.isChecked() == True:
            self.type_servo = 0
        if self.radio_fermeture_servo.isChecked() == True:
            self.type_servo = 1

    def fermeture_servo(self):
        print('fermeture servo')
    def radioBouton_electro(self):
        self.type_electro = 0
        if self.radio_ouverture_electro.isChecked() == True:
            self.type_electro = 0
        if self.radio_fermeture_electro.isChecked() == True:
            self.type_electro = 1

    def commande_purge_pompes(self):
        print('purge')


app = QApplication(sys.argv)
