import subprocess
import sys
import glob
import cv2
import serial
import time
from Logiciel.pi_controller.HMI2.inverseKinematic import scaraRobot
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
                        dataIn = str(self.arduino.readline())
                        # print(dataIn)
                        if dataIn.find("Done") != -1:
                            done=True
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
        self.moveTo(0.49,0,wait)
        self.moveUpDown(15, wait)
        return

    def activatePompe(self,list_pompe, list_quant,wait):
        # G101:A1.5 pour la pompe 1 avec 1.5oz
        print(list_pompe)
        print(list_quant)

        for i in range(len(list_pompe)):
            pompe = "G10" + str(list_pompe[i]) + ":A" + str(list_quant[i]) + "\r\n"
            self.send_message(pompe,wait)
            #livreIngredient.update_Quantite(index,quantite)
        return


    def sequence(self,recette,livreIngredient):
        wait=True
        self.moveUpDown(15,wait)
        self.moveTo(0.49,0,wait)

        if self.calib.calib_vision_seuil is False:
            return "Veuillez recalibrer la caméra dans la fenêtre réglage"
        else:
            positionVerre=self.vision()
            print(positionVerre)

            if(self.r.isInEnvloppe(positionVerre) is False):
                return "Verre inaccessible! Êtes vous trop chôoo?\nPlacez votre verre et recommander"

            if(positionVerre[0]==0 and positionVerre[1]==0):
                return "Aucun verre détecté! Êtes vous trop chôoo?\nPlacez votre verre et recommander"
            else:

                #self.moveTo(0.36,0.10,wait)
                self.servo(180,wait)
                self.moveUpDown(60, wait)
                self.moveTo(0.47, 0.04, wait)
                self.moveTo(0.285,-0.03,wait)
                if (self.pompe(recette,livreIngredient,wait) is False):
                    self.moveTo(0.47, 0.04, wait)
                    self.servo(5, wait)
                    return "Quantité insuffisante d'un ingrédient"
                else:
                    time.sleep(5)
                    #self.moveTo(0.49,0,wait)
                    self.moveTo(0.47,0.04,wait)
                    self.servo(5,wait)
                    self.moveUpDown(210,wait)
                    self.moveTo(0.40, 0.25, wait)
                    self.shake(wait)


                    #positionVerre=[-0.15, 0.4]
                    pos = self.r.tangentAuVerre(positionVerre)
                    self.moveTo(pos[0],pos[1],wait)
                    self.servo(40,wait)

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
        self.list_quantite_ingredient_dispo = livreIngredient.get_list_quantite().copy()
        self.list_pos_bouteille = livreIngredient.get_list_position().copy()

        self.list_ingredient = recette.getlistAlcool().copy()
        self.list_quantite = recette.getlistQuantite().copy()

        for i in range(len(self.list_ingredient)):
            for j in range(len(self.list_ingredient_dispo)):
                if self.list_ingredient_dispo[j] == self.list_ingredient[i]:
                    if float(self.list_quantite_ingredient_dispo[j])<float(self.list_quantite[i]):
                        return False
                    else:
                        self.list_position_pompe.append(self.list_pos_bouteille[j])
                        self.list_quant_pompe.append(self.list_quantite[i])
                        # remove from next search
                        #self.list_ingredient_dispo.pop(j)
                        #self.list_pos_bouteille.pop(j)


        return [self.list_position_pompe, self.list_quant_pompe]


    def pompe(self,recette, livreIngredient,wait):
        list_pompe_quantite=self.identification_pompe(recette, livreIngredient)
        if( list_pompe_quantite is False):
            return False
        else:
            livreIngredient.update_Quantite(list_pompe_quantite[0],list_pompe_quantite[1],livreIngredient)
            self.activatePompe(list_pompe_quantite[0],list_pompe_quantite[1],wait)
            return True

    def shake(self,wait):
        self.send_message("M3\r\n",wait)

    def vision(self):
        output = True  # False: Disable display output & True: Enable display output
        calib = False
        subprocess.call('sudo fswebcam -r 2048x1536 /home/pi/Desktop/Vision.jpeg', shell=True)
        path = r'/home/pi/Desktop/Vision.jpeg'

        resize_factor = 10
        imcolor = Image.open(path)
        im = (imcolor.convert('L'))
        im = im.resize((int(im.size[0] / resize_factor), int(im.size[1] / resize_factor)))
        pixel = im.load()

        nb_line = 10
        y_start = [10, 10, 10, 10, 10, 10, 10, 10, 10]  # [75,50,30,25,22,25,33,50,80]
        y_end = [100, 100, 100, 100, 100, 100, 100, 100, 95]
        x_space = int(im.size[0] / nb_line)
        pixel_seuil = 45
        seuil = 210
        y_center = 0
        x_center = 0
        end_vr = False
        vr = 2

        for i in range(1, nb_line):
            if end_vr:
                print(0)
            # im.putpixel([(i*x_space),y_start[i-1]],150)
            for j in range(y_start[i - 1], y_end[i - 1]):
                if end_vr:
                    print(0)
                    # break
                if pixel[(i * x_space), j + vr] > seuil:  # -pixel[(i*x_space),(j)]>pixel_seuil:# or pixel[(i*x_space),(j)]>245:
                    print('test')
                    y1 = j
                    j = j + 1
                    # im.putpixel([(i*x_space),j],0)
                    while (pixel[(i * x_space), j] - pixel[(i * x_space), (j + vr)]) < pixel_seuil and j < (
                            im.size[1] - 50):
                        y_center = int(j - ((j - y1) / 2))
                        # im.putpixel([(i*x_space),j],0)
                        j = j + 1
                    x = i * x_space
                    # print(x)
                    # print(pixel[(x),y_center])
                    while (pixel[(x), y_center] - pixel[(x + vr), y_center]) < pixel_seuil and x < (im.size[0] - 5):
                        x1 = x
                        # im.putpixel([x,y_center],0)
                        x = x + 1
                    x = i * x_space
                    while (pixel[(x), y_center] - pixel[(x - vr), y_center]) < pixel_seuil and x > 5:
                        x_center = int(x1 - ((x1 - x) / 2))
                        # im.putpixel([x,y_center],0)
                        x = x - 1
                    y = y_center
                    while (pixel[(x_center), y] - pixel[(x_center), (y + vr)]) < pixel_seuil and y < (im.size[1] - 50):
                        y1 = y
                        # im.putpixel([x_center,y],0)
                        y = y + 1
                    y = y_center
                    while (pixel[(x_center), y] - pixel[(x_center), (y - vr)]) < pixel_seuil and y > y1:
                        y_center = int(y1 - ((y1 - y) / 2))
                        # im.putpixel([x_center,y],0)
                        y = y - 1
                        end_vr = True
                    break

        if y_center != 0:
            y_center = y_center + vr
        if calib:
            for i in range(1, nb_line):
                for j in range(y_start[i - 1], y_end[i - 1]):
                    im.putpixel([(i * x_space), j], 0)
            print(im.size[0])
            print(im.size[1])
            # im.show()

        size_square = 2
        if output:
            if (x_center != 0 and y_center != 0):
                for i in range(x_center - size_square, x_center + size_square, 1):
                    for j in range(y_center - size_square, y_center + size_square, 1):
                        im.putpixel([i, j], 0)
            im.show()
        coord = [0, 0]
        if (x_center != 0 and y_center != 0):
            coord = [-(x_center * (-0.003444444) + 0.3065),
                     (y_center * (-0.0034) + 0.4258)]  # [x,y] in meters, origin at the A axis
        """
        r = np.sqrt(coord[0]**2 + (coord[1]-0.13)**2)
        r1 = 0.98
        r2 = 0.95
        r3 = 0.90
        if r>0.8 and r<0.18:
            coord = [coord[0]*r1,coord[1]*r1]
        elif r>=0.18 and r<0.22:
            coord = [coord[0]*r2,coord[1]*r2]
        else:
            coord = [coord[0]*r3,coord[1]*r3]
        """
        return coord

