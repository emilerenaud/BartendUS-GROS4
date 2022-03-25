import cv2
import math
import numpy as np
from matplotlib import pyplot as plt
import time

class Calibration_cam():
    # Classe permettant de calibrer la caméra sur le robot en fonction
    # des 3 points de repères présents sur la plateforme


    def __init__(self):
        self.liste_coord_centres_ref = []
        self.liste_points_coord_centre = []
        self.seuil = 5
        self.get_data_from_reference()      # Appel de la fonction pour aller chercher les datas de l'image de référence


    def get_data_from_reference(self):
        # Recherche des centres des cercles sur l'image de référence:
        path = "/home/pi/Pictures/img_reference_calib.png"
        img_reference = cv2.imread(path)

        # Conversion de l'image en noir et blanc:
        gray = cv2.cvtColor(img_reference, cv2.COLOR_BGR2GRAY)

        # Spécification des valeurs limites (pixel = 0 si < 100 et pixel = 1 si > 255) pour en sortir une image binaire
        _, image_binaire = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

        # Trouver les contours de l'image binaire
        contours, _ = cv2.findContours(image_binaire, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        i = 0
        for c in contours:
            liste_points_ref = []
            perimeter = cv2.arcLength(c, True)

            # Filtrer les perimètres trop petits:
            if perimeter >= 50:
                # Ignorer le premier contour pusique la fonction "findcontour" détecte l'image complète comme premier élément
                if i == 0:
                    i = 1
                    continue

                # Approximer les formes
                approx = cv2.approxPolyDP(c, 0.01 * cv2.arcLength(c, True), True)

                # Déssiner les contours sur l'image
                # cv2.drawContours(img_reference, [c], -1, (0, 255, 0), 2)

                # Trouver le centre des contours
                M = cv2.moments(c)
                if M['m00'] != 0.0:
                    x = int(M['m10'] / M['m00'])
                    liste_points_ref.append(x)
                    y = int(M['m01'] / M['m00'])
                    liste_points_ref.append(y)
                    self.liste_coord_centres_ref.append(liste_points_ref)

                # Ajout d'un point sur l'image au centre des contours
                cv2.circle(img_reference, (x, y), radius=3, color=(0, 0, 255), thickness=-1)
            else:
                continue

        plt.imshow(img_reference, cmap="gray")
        plt.show()

        cv2.waitKey(0)
        cv2.destroyAllWindows()



    def calib_vision_init(self):
        # Afficher les centre des 3 points sur l'image en temps réel:
        # Prendre une photo:
        cv2.namedWindow("Calibration")
        cap = cv2.VideoCapture(0)       # Identifier le bon port de caméra -> 0 ou 1 normallement

        # Vérifier que l'ouverture de la caméra se fait correctement:
        if cap.isOpened():
            rval, img_reel_time = cap.read()
        else:
            rval = False
            print("ERREUR - Ne peut pas ouvrir la caméra!")


        # while rval and cv2.getWindowProperty("Calibration", cv2.WND_PROP_VISIBLE):
        while rval:
            for center in self.liste_coord_centres_ref:
                cv2.circle(img_reel_time, (center[0], center[1]), radius = 4, color = (0, 0, 255), thickness = -1)
            cv2.imshow("Calibration", img_reel_time)
            rval, img_reel_time = cap.read()


            # print(cv2.getWindowProperty("Calibration"), 1)

            # if cv2.getWindowProperty("Calibration", cv2.WND_PROP_VISIBLE):
            #     print("Timer on")
            #     time.sleep(500)
            #     print("Timer done")
            #     break

            k = cv2.waitKey(1) & 0xFF
            if k == 27:  # Fermeture de la fenêtre avec la touche "ESC" ou le "X" du GUI
                break

        cv2.destroyAllWindows()
        cap.release()



    def calib_vision_seuil(self):
        # Prendre une photo:
        cv2.namedWindow("Calibration_seuil")
        cap = cv2.VideoCapture(0)

        if cap.isOpened():
            rval, img_to_verify = cap.read()
        else:
            rval = False
            print("ERREUR - Ne peut pas ouvrir la caméra!")

        # converting image into grayscale image
        gray = cv2.cvtColor(img_to_verify, cv2.COLOR_BGR2GRAY)

        plt.imshow(gray, cmap="gray")
        plt.show()

        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # setting threshold of gray image
        _, threshold = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

        # using a findContours() function
        contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        i = 0
        # list for storing names of shapes
        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            liste = []
            if i == 0:
                i = 1
                continue

            approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)

            # # using drawContours() function
            # cv2.drawContours(img_to_verify, [contour], -1, (0, 255, 0), 2)

            # finding center point of shape
            M = cv2.moments(contour)
            if M['m00'] != 0.0:
                x = int(M['m10'] / M['m00'])
                liste.append(x)
                y = int(M['m01'] / M['m00'])
                liste.append(y)
                self.liste_points_coord_centre.append(liste)

        for j, point in self.liste_points_coord_centre:
            if not(self.liste_coord_centres_ref[j][0] - self.seuil <= point[0] <= \
                   self.liste_coord_centres_ref[j][0] - self.seuil):
                print("CALIBRATION NÉCESSAIRE: Coordonnée en X ne respecte pas le seuil")
                return False

            elif not (self.liste_coord_centres_ref[j][1] - self.seuil <= point[1] <= \
                      self.liste_coord_centres_ref[j][1] - self.seuil):
                print("CALIBRATION NÉCESSAIRE: Coordonnée en Y ne respecte pas le seuil")
                return False

        plt.imshow(img_to_verify, cmap="gray")
        plt.show()

        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return True



if __name__ == '__main__':
    calib = Calibration_cam()
    calib.calib_vision_init()

    # calib.calib_vision_seuil()
    # calib_vision_seuil()
    # calib.calib_vision_init
    print('Done with vision')
