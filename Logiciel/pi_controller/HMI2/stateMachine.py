
import sys
import glob
import serial
import time
from Logiciel.pi_controller.HMI2.inverseKinematic import scaraRobot

class sequence():

    # def send_message(x):
    #     arduino.write(bytes(x, 'utf-8'))
    #     time.sleep(0.5)
    #     data = arduino.readline()
    #     return data

    def __init__(self):
        #raspPi : '/dev/ttyUSB0'
        #ordi : port=COM3
        # self.arduino = serial.Serial(port='COM5', baudrate=9600, timeout=.1)     # Pour le Pi
        # self.arduino = serial.Serial(port='COM6', baudrate=9600, timeout=.1)
        self.r= scaraRobot()

    def openSerial(self):
        # open the serial port selon lui qui a ete choisi dans le ComboBox du HMI.
        self.arduino = serial.Serial(port='COM5', baudrate=9600, timeout=.1)

    def send_message(self, x):
        self.arduino.write(bytes(x, 'utf-8'))
        time.sleep(0.05)
        print("data sent")
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
                print("mauvais message")

            # print("while not done")
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
        self.r.inverseKinematic([x, y])
        angles = self.r.getAngleDeg()
        position = "G0:A" + str(angles[0]) + ":B" + str(angles[1]) + "\r\n"
        print(position)
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

    def activatePompe(self,list_pompe, list_quant):
        # G101:A1.5 pour la pompe 1 avec 1.5oz
        for i in list_pompe:
            pompe = "G10" + str(list_pompe[i]) + ":A" + str(list_quant[i]) + "\r\n"

            self.send_message(pompe)
            return


    def sequence(self):
        self.homing()
        print("home done")
        #self.moveUpDown(45)
        #print("z done")
        #0.4Y 0.15X
        self.moveUpDown(170)
        pos = self.r.tangentAuVerre([-0.15, 0.4])
        if(pos is not False):

            self.moveTo(pos[0],pos[1])

            #print("home done")
            time.sleep(0)

            self.poignet(-70)
            self.servo(45)
            sens = self.r.getSensVersement()
            self.versement(sens)
            self.servo(5)
            #print("servo")
            #self.servo(5)
            #self.moveTo(0,0.45)
            #self.servo(150)
            #self.versement()

    def versement(self,sens):
        # caller la fonction HOME
        if sens == "gauche":
            versementMessage = "M4\r\n"
        else:
            versementMessage = "M5\r\n"
        self.send_message(versementMessage)
        return
    # retourne la position et le temps de chacune des pompes a actionner
    def identification_pompe(self,recette, livreIngredient):
        conv=0.5
        list_position_pompe = []
        list_quant_pompe = []

        list_ingredient_dispo = livreIngredient.get_list_ingredient().copy()
        list_pos_bouteille = livreIngredient.get_list_position().copy()

        list_ingredient = recette.getlistAlcool()
        list_quantite = recette.getlistQuantite()

        for i in range(len(list_ingredient)):
            for j in range(len(list_ingredient_dispo)):
                if list_ingredient_dispo[j] == list_ingredient[i]:
                    list_position_pompe.append(list_pos_bouteille[j])
                    list_quant_pompe.append(list_quantite[i])
                    # remove from next search
                    list_ingredient_dispo.pop(j)
                    list_pos_bouteille.pop(j)
                    break

        return [list_position_pompe, list_quant_pompe]


    def pompe(self,recette, livreIngredient):
        list_pompe_quantite=self.identification_pompe(recette, livreIngredient)
        self.activatePompe(list_pompe_quantite[0],list_pompe_quantite[1])



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