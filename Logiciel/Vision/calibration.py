# import picamera
import cv2
import math
import numpy as np
from matplotlib import pyplot as plt
import time

def calib_vision():
    # Fonction permettant de calibrer la caméra sur le robot en fonction
    # des 3 points de repères présents sur la plateforme

    # Recherche des centres des cercles sur l'image de référence:
    img_reference = cv2.imread('img_reference_calib.png')

    # Conversion de l'image en noir et blanc:
    gray = cv2.cvtColor(img_reference, cv2.COLOR_BGR2GRAY)

    # Spécification des valeurs limites (pixel = 0 si < 100 et pixel = 1 si > 255) pour en sortir une image binaire
    _, image_binaire = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

    # Trouver les contours de l'image binaire
    contours, _ = cv2.findContours(image_binaire, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    i = 0
    liste_coord_centres = []
    for c in contours:
        liste_points = []
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
                liste_points.append(x)
                y = int(M['m01'] / M['m00'])
                liste_points.append(y)
                liste_coord_centres.append(liste_points)

            # Ajout d'un point sur l'image au centre des contours
            cv2.circle(img_reference, (x, y), radius = 3, color = (0, 0, 255), thickness = -1)
        else:
            continue

    plt.imshow(img_reference, cmap="gray")
    plt.show()

    cv2.waitKey(0)
    cv2.destroyAllWindows()



    # Afficher les centre des 3 pints sur l'image en temps réel:
    # Prendre une photo:
    # ** SOUS Unix **
    # cap = PiCamera()
    # time.sleep(2)                                 # Attendre que la caméra s'initialise
    # cap.capture("/home/pi/Pictures/img.jpg")
    # print("Photo prise")

    # ** SOUS Windows **
    cv2.namedWindow("Calibration")
    cap = cv2.VideoCapture(0)       # Identifier le bon port de caméra -> 0 ou 1 normallement

    # Vérifier que l'ouverture de la caméra se fait correctement:
    if cap.isOpened():
        rval, img_reel_time = cap.read()
    else:
        rval = False
        print("ERREUR - Ne peut pas ouvrir la caméra!")

    while rval and cv2.getWindowProperty("Calibration", cv2.WND_PROP_VISIBLE):
        for center in liste_coord_centres:
            cv2.circle(img_reel_time, (center[0], center[1]), radius = 4, color = (0, 0, 255), thickness = -1)
        cv2.imshow("Calibration", img_reel_time)
        rval, img_reel_time = cap.read()

        k = cv2.waitKey(1) & 0xFF
        if k == 27:  # Fermeture de la fenêtre avec la touche "ESC" ou le "X" du GUI
            break

    cv2.destroyAllWindows()
    cap.release()

if __name__ == '__main__':
    calib_vision()
