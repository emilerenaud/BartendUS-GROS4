from PyQt5.QtWidgets import QRadioButton

from test_presentation import Ui_MainWindow

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from inverseKinematic import scaraRobot
import serial
import time

class PresentationWindow(qtw.QWidget, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.bouton_GO.clicked.connect(self.depart_robot)
        self.ui.bouton_ESTOP.clicked.connect(self.arret_robot)

        self.ui.bouton_VERRE.clicked.connect(self.deplacement_au_verre)
        self.ui.HOME.clicked.connect(self.Home)

        #radio bouton
        self.ui.bouton_LINEAIRE.clicked.connect(self.activer_actionneur)
        self.ui.lin_1.setChecked(True)
        self.r=scaraRobot()
        self.arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)

    def write_read(self,x):
        arduino.write(bytes(x, 'utf-8'))
        time.sleep(0.5)
        data = self.arduino.readline()
        return data

    def Home(self):
        #caller la fonction HOME
         homing = "G2\r\n"
         write_read(testString)
        qtw.QMessageBox.information(self, 'Success', 'Le robot se déplace vers HOME.')

    def deplacement_au_verre(self):
        #caller la fonction de depart

        qtw.QMessageBox.information(self, 'Success', 'Le robot se déplace vers le verre selon les coordonnées obtenues par la caméra.')

    def arret_robot(self):
        # caller la fonction de ESTOP
        qtw.QMessageBox.critical(self, 'Fail', 'Le ESTOP a été appuyé.')


    def depart_robot(self):
        string_position_X = self.ui.position_X.text()
        string_position_Y = self.ui.position_Y.text()
        string_position_Z = self.ui.position_Z.text()

        if string_position_X.isdecimal() and string_position_Y.isdecimal() and string_position_Z.isdecimal():
            position_X = int(string_position_X)
            position_Y = int(string_position_Y)
            position_Z = int(string_position_Z)

            r.inverseKinematic(position_X,position_Y)
            angles=r.getAngleDeg()
            aAngle = angles[1]
            bAngle = angles[2]
            position = "G0:A" + str(aAngle) + ":B" + str(bAngle) + ":Z" + 0 + "\r\n"
            value = write_read(position)
            print(value)
        else:
            print('''Les positions ne sont pas des chiffres ou certaines boites n'ont pas de valeur de entré.''')

        if (position_X and position_Y) <= 5 and position_Z <= 6:
            #caller la fonction de déplacement avec les bonnes positions

            qtw.QMessageBox.information(self, 'Success', 'Le robot peut aller à la position donnée.')

        else:
            qtw.QMessageBox.critical(self, 'Fail', 'Le robot ne peut pas se rendre à la position donnée.')

    def activer_actionneur(self):
        self.indice_actionneur = 0

        if self.ui.lin_1.isChecked() == True:
            self.indice_actionneur = 1
            # caller la fonction pour activer lin 1
            print(self.indice_actionneur)
        if self.ui.lin_2.isChecked() == True:
            self.indice_actionneur = 2
            # caller la fonction pour activer lin 2
            print(self.indice_actionneur)
        if self.ui.lin_3.isChecked() == True:
            self.indice_actionneur = 3
            # caller la fonction pour activer lin 3
            print(self.indice_actionneur)
        if self.ui.lin_4.isChecked() == True:
            self.indice_actionneur = 4
            # caller la fonction pour activer lin 4
            print(self.indice_actionneur)


if __name__ == '__main__':
    app = qtw.QApplication([])

    w = PresentationWindow()
    w.show()

    app.exec_()