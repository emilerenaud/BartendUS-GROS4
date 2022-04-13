from PyQt5.QtWidgets import QRadioButton

from test_presentation import Ui_MainWindow

from PyQt5 import QtWidgets as qtw
from inverseKinematic import scaraRobot
import serial
import time

# import numpy as np
# from PIL import Image
# import cv2

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
        self.arduino.write(bytes(x, 'utf-8'))
        time.sleep(0.5)
        data = self.arduino.readline()
        return data

    def Home(self):
        #caller la fonction HOME
        homing = "G2\r\n"
        self.write_read(homing)
        qtw.QMessageBox.information(self, 'Success', 'Le robot se déplace vers HOME.')

    def deplacement_au_verre(self):
        position=self.vision()
        position_X=position[0]
        position_Y=position[1]
        self.r.inverseKinematic(position_X, position_Y)
        angles = self.r.getAngleDeg()
        aAngle = angles[0]
        bAngle = angles[1]
        position = "G0:A" + str(aAngle) + ":B" + str(bAngle) + ":Z" + str(0) + "\r\n"
        value = self.write_read(position)
        #    print(value)
        ##else:
        #  print('''Les positions ne sont pas des chiffres ou certaines boites n'ont pas de valeur de entré.''')

        if self.r.inverseKinematic(position_X, position_Y) is not False:
            # caller la fonction de déplacement avec les bonnes positions

            qtw.QMessageBox.information(self, 'Success', 'Le robot peut aller à la position donnée.')

        else:
            qtw.QMessageBox.critical(self, 'Fail', 'Le robot ne peut pas se rendre à la position donnée.')
        #caller la fonction de depart

        qtw.QMessageBox.information(self, 'Success', 'Le robot se déplace vers le verre selon les coordonnées obtenues par la caméra.')

    def arret_robot(self):
        # caller la fonction de ESTOP
        qtw.QMessageBox.critical(self, 'Fail', 'Le ESTOP a été appuyé.')


    def depart_robot(self):
        string_position_X = self.ui.position_X.text()
        string_position_Y = self.ui.position_Y.text()
        string_position_Z = self.ui.position_Z.text()
        position_X = 0
        position_Y = 0
        position_Z = 0
        #if string_position_X.isdecimal() and string_position_Y.isdecimal() and string_position_Z.isdecimal():
        position_X = float(string_position_X)
        position_Y = float(string_position_Y)
        position_Z = float(string_position_Z)

        self.r.inverseKinematic(position_X,position_Y)
        angles=self.r.getAngleDeg()
        aAngle = angles[0]
        bAngle = angles[1]
        position = "G0:A" + str(aAngle) + ":B" + str(bAngle) + ":Z" + str(0)+ "\r\n"
        value = self.write_read(position)
        #    print(value)
        ##else:
          #  print('''Les positions ne sont pas des chiffres ou certaines boites n'ont pas de valeur de entré.''')

        if self.r.inverseKinematic(position_X,position_Y) is not False:
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

    # def vision(self):
    #     cap = cv2.VideoCapture(0)
    #     if not cap.isOpened():
    #         raise IOError("Cannot open webcam")
    #     # while True:
    #     ret, frame = cap.read()
    #
    #     #frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    #     #     c = cv2.waitKey(1)
    #     #     if c == 27:
    #     #         break
    #
    #     cap.release()
    #     #cv2.destroyAllWindows()
    #     im = frame
    #     pixel = im.load()
    #     x =0
    #     y =0
    #     nb =0
    #     for i in range(im.size[0]):
    #         for j in range(im.size[1]):
    #             if pixel[i,j] > 150:
    #                 im.putpixel([i,j], 255)
    #                 x += i
    #                 nb += 1
    #                 y += j
    #             else:
    #                 im.putpixel([i,j], 0)
    #
    #     x = int(x/nb)
    #     y = int(y/nb)
    #     coord = [x, y]
    #     return coord

def wait_for_done():
    time.sleep(0.5)
    messageIn = arduino.readline()
    if(messageIn)

    return data

def send_message(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.5)
    data = arduino.readline()
    return data

# en deg
def poignet(angle):
    position = "G4:A" + str(angle) + "\r\n"
    value = send_message(position)
    if wait_for_done()is False:
        wait_for_done()


    return

def servo(angle):
    position = "G5:A" + str(angle) + "\r\n"
    value = send_message(position)
    return

def electro(activate):
    if activate:
        position = "M1" + "\r\n"
        value = send_message(position)
    else:
        position = "M0" + "\r\n"
        value = send_message(position)
    return

    # z est en mm

def moveUpDown(z):
    position = "G3:Z" + str(z) + "\r\n"
    value = send_message(position)
    return

def moveTo(x, y):
    r.inverseKinematic(x, y)
    angles = r.getAngleDeg()
    position = "G0:A" + str(angles[0]) + ":B" + str(angles[1]) + "\r\n"
    value = send_message(position)
    return



def homing():
    # caller la fonction HOME
    homing = "G2\r\n"
    send_message(homing)
    return

def versement():
    poignet(120)
    moveUpDown(20)

# if __name__ == '__main__':
#
#     r=scaraRobot()
#     arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)
#
#     homing()
#     moveUpDown(45)
#     moveTo(0.45,0)
#     servo(150)
#     time.sleep(2)
#     servo(5)
#     moveTo(0,0.45)
#     servo(150)
#     versement()








