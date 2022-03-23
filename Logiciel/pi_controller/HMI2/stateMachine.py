

import serial
import time
import sys
from inverseKinematic import scaraRobot

class communication():

    def __init__(self):
        self.arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)
        self.r= scaraRobot()
    # def wait_for_done():
    #     time.sleep(0.5)
    #     messageIn = arduino.readline()
    #     if (messageIn)
    #
    #     return data

    def send_message(self, x):
        self.arduino.write(bytes(x, 'utf-8'))
        time.sleep(0.05)
        while(self.arduino.readline()!="Done"):
            time.sleep(0.05)
        return

    # en deg
    def poignet(self,angle):
        position = "G4:A" + str(angle) + "\r\n"
        self.send_message(position)
        return

    def servo(self,angle):
        position = "G5:A" + str(angle) + "\r\n"
        self.send_message(position)
        return

    def electro(self,activate):
        if activate:
            position = "M1" + "\r\n"
            self.send_message(position)
        else:
            position = "M0" + "\r\n"
            self.send_message(position)
        return

    def moveUpDown(self,z):
        position = "G3:Z" + str(z) + "\r\n"
        self.send_message(position)
        return

    def moveTo(self,x, y):
        self.r.inverseKinematic(x, y)
        angles = self.r.getAngleDeg()
        position = "G0:A" + str(angles[0]) + ":B" + str(angles[1]) + "\r\n"
        self.send_message(position)
        return

    def homing(self):
        # caller la fonction HOME
        homing = "G2\r\n"
        self.send_message(homing)
        return

    # def versement():
    #     poignet(120)
    #     moveUpDown(20)

    def activatePompe(self,list_pompe, list_temps):
        # G101:A1.5 pour la pompe 1 avec 1.5oz
        for i in list_pompe:
            pompe = "G10" + str(list_pompe[i]) + ":A" + str(list_temps[i]) + "\r\n"
            self.send_message(pompe)
            return



    # retourne la position et le temps de chacune des pompes a actionner
def sequence_pompe(recette, livreIngredient):
    list_position_pompe = []
    list_temps_pompe = []

    list_ingredient_dispo = livreIngredient.list_ingredient
    list_pos_bouteille = livreIngredient.list_position

    list_ingredient = recette.getlistAlcool()
    list_quantite = recette.getlistQuantite()

    for i in range(len(list_ingredient)):
        for j in range(len(list_ingredient_dispo)):
            if list_ingredient_dispo[j] == list_ingredient[i]:
                list_position_pompe.append(list_pos_bouteille[j])
                list_temps_pompe.append(convTempsQuantite(list_quantite[i]))
                # remove from next search
                list_ingredient_dispo.pop(j)
                list_pos_bouteille.pop(j)

    return [list_position_pompe, list_temps_pompe]

def convTempsQuantite(quantiteOz):
    facteurConv = 0.5
    return quantiteOz * facteurConv

#***************************************A executer pour tester la vision FRED
# com= communication()
# com.homing()
# com.moveTo(vision())






#1 sequence
#     homing()
#     moveUpDown(45)
#     moveTo(0.45,0)
#     servo(150)
#     time.sleep(2)
#     servo(5)
#     moveTo(0,0.45)
#     servo(150)
#     versement()