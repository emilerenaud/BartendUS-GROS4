import subprocess
import sys
import glob
import cv2
import serial
import time
from pi_controller.HMI2.inverseKinematic import scaraRobot
from Vision.calibration import Calibration_cam
from PIL import Image
import subprocess
import numpy as np

class sequence():

    def __init__(self):
        #raspPi : '/dev/ttyUSB0'    #ordi : port=COM3
        #self.arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)     # Pour le Pi
        self.r= scaraRobot()
        self.calib = Calibration_cam



    def send_message(self, message,wait):
        try:
            print(message)
            #self.arduino.reset_input_buffer()
            self.arduino.write(bytes(message, 'utf-8'))
            time.sleep(0.05) # one tick delay (15ms) in between reads for stability
            print("data sent")

            if wait :
                done=False
                while(not done):
                    try :
                        # print(self.arduino.readline())
                        dataIn = str(self.arduino.readline())
                        # print(dataIn)
                        if dataIn.find("Done") != -1:
                            print("message recu")
                            done=True
                        # else:
                        #     print("wrong message")
                    except:
                        done=False

                    time.sleep(0.05)
        except:
            print("erreur aucun port sélectionné")
        return

    def openSerial(self, port_com):
        # open the serial port selon lui qui a ete choisi dans le ComboBox du HMI.
        try:
            self.arduino = serial.Serial(port=port_com, baudrate=9600, timeout=.1)
            time.sleep(0.5)
            self.arduino.reset_input_buffer()
            self.send_message("M11\r\n", False)


        except:
            pass
    
    # en deg
    def poignet(self,angle,wait):
        position = "G4:A" + str(angle) + "\r\n"
        self.send_message(position,wait)
        return

    def servo(self,angle,wait):
        position = "G5:A" + str(angle) + "\r\n"
        self.send_message(position,wait)
        return

    def electro(self,activate,wait):
        if activate:
            position = "M1" + "\r\n"
            self.send_message(position,wait)
        else:
            position = "M0" + "\r\n"
            self.send_message(position,wait)
        return

    def moveUpDown(self,z,wait):
        position = "G3:Z" + str(z) + "\r\n"
        self.send_message(position,wait)
        return

    def moveTo(self,x, y,wait):
        self.r.inverseKinematic([x, y])
        angles = self.r.getAngleDeg()
        print(x,y)
        print(angles)
        position = "G0:A" + str(angles[0]) + ":B" + str(angles[1]) + "\r\n"
        print(position)
        self.send_message(position,wait)
        return

    def homing(self,wait):
        # caller la fonction HOME
        homing = "G2\r\n"
        self.send_message(homing,wait)
        return

    def activatePompe(self,list_pompe, list_quant,wait):
        # G101:A1.5 pour la pompe 1 avec 1.5oz
        print(list_pompe)
        print(list_quant)

        for i in range(len(list_pompe)):
            print(str(list_pompe[i]))
            print(str(list_quant[i]))
            pompe = "G10" + str(list_pompe[i]) + ":A" + str(list_quant[i]) + "\r\n"
            print(pompe)
            self.send_message(pompe,wait)
        return


    def sequence(self,recette,livreIngredient):
        wait=True
        self.moveUpDown(70,wait)
        self.moveTo(0.49,0,wait)

        if self.calib.calib_vision_seuil is False:
            return "Veuillez recalibrer la caméra dans la fenêtre réglage"
        else:
            positionVerre=self.vision()
            time.sleep(2)
            if(positionVerre[0]==0 and positionVerre[1]==0):
                return "Aucun verre détecté, placez vos verres "
            else:
                self.moveTo(0.36,0.10,wait)
                self.servo(170,wait)
                self.moveTo(0.34,-0.03,wait)
                if (self.pompe(recette,livreIngredient,wait) is False):
                    return "Quantité insuffisante d'un ingrédient"
                else:
                    time.sleep(6)
                    #self.moveTo(0.49,0,wait)
                    self.moveTo(0.36,0.14,wait)
                    self.servo(5,wait)
                    self.moveUpDown(200,wait)
                    self.shake(wait)
                    #positionVerre=[-0.15, 0.4]
                    pos = self.r.tangentAuVerre(positionVerre)
                    self.moveTo(pos[0],pos[1],wait)
                    self.servo(150,wait)

                    sens = self.r.getSensVersement()
                    if(sens=="gauche"):
                        self.poignet(70,wait)
                    else:
                        self.poignet(-70,wait)

                self.versement(sens,wait)
                self.servo(5,wait)
                self.moveTo(0.49, 0, wait)
                return ""

    def versement(self,sens,wait):
        # caller la fonction HOME
        if sens == "gauche":
            versementMessage = "M4\r\n"
        else:
            versementMessage = "M5\r\n"
        self.send_message(versementMessage,wait)
        return
    
    # retourne la position et le temps de chacune des pompes a actionner
    def identification_pompe(self,recette, livreIngredient):
        conv=0.5
        print(recette)
        self.list_position_pompe = []
        self.list_quant_pompe = []

        self.list_ingredient_dispo = livreIngredient.get_list_ingredient().copy()
        self.list_pos_bouteille = livreIngredient.get_list_position().copy()

        self.list_ingredient = recette.getlistAlcool().copy()
        self.list_quantite = recette.getlistQuantite().copy()

        for i in range(len(self.list_ingredient)):
            for j in range(len(self.list_ingredient_dispo)):
                if self.list_ingredient_dispo[j] == self.list_ingredient[i]:
                    self.list_position_pompe.append(self.list_pos_bouteille[j])
                    self.list_quant_pompe.append(self.list_quantite[i])
                    # remove from next search
                    self.list_ingredient_dispo.pop(j)
                    self.list_pos_bouteille.pop(j)
                    break

        return [self.list_position_pompe, self.list_quant_pompe]


    def pompe(self,recette, livreIngredient,wait):
        list_pompe_quantite=self.identification_pompe(recette, livreIngredient)
        if( list_pompe_quantite is False):
            return False
        else:
            self.activatePompe(list_pompe_quantite[0],list_pompe_quantite[1],wait)
            return True

    def shake(self,wait):
        self.send_message("M3\r\n",wait)

    def vision(self):
        output = True  # False: Disable display output & True: Enable display output
        subprocess.call('sudo fswebcam -r 2048x1536 /home/pi/Desktop/Vision.jpg', shell=True)
        path = r'/home/pi/Desktop/Vision.jpg'

        size = 480
        imcolor = Image.open(path)
        im = (imcolor.convert('L')).resize((size, size))
        pixel = im.load()

        r = 200
        top = 75
        nb_point = 10
        bottom = 420
        a = -r / ((bottom / 2) ** 2)
        np_point_useless = 1
        seuil = 50
        y2 = (np.arange(nb_point) - nb_point / 2) * (bottom / nb_point)
        x2 = abs(a * (y2 ** 2) - top)
        y2 = y2 + size / 2
        for i in range(im.size[0]):
            if i < 430:
                if i > 50:
                    for j in range(0, int(abs(a * ((i - 240) ** 2) - top))):
                        im.putpixel([i, j], 0)
            else:
                for j in range(im.size[1]):
                    im.putpixel([i, j], 0)
            if i < 51:
                for j in range(im.size[1]):
                    im.putpixel([i, j], 0)

        x = 0
        y = 0
        nb = 1
        r = 0.40
        for i in range(im.size[0]):
            for j in range(im.size[1]):
                if j > (im.size[1] - 150):
                    im.putpixel([i, j], 0)
                elif j < (0):
                    im.putpixel([i, j], 0)
                elif i > (im.size[0] - 0):
                    im.putpixel([i, j], 0)
                elif i < (0):
                    im.putpixel([i, j], 0)
                elif pixel[i, j] > 200:
                    x += i
                    nb += 1
                    y += j
        x = int(x / nb)
        y = int(y / nb)
        coord = [((((x - (im.size[0] / 2)))) * (0.19 + 0.17) / (122 + 114)) + 0.003898, (
                    abs(y - im.size[1]) * (31 - 12) / (
                        354 - 181) - 7.878) / 100]  # [x,y] in meters, origin at the A axis
        if output:
            for i in range(x - 2, x + 2, 1):
                for j in range(y - 2, y + 2, 1):
                    im.putpixel([i, j], 0)
            im.show()
        return coord

