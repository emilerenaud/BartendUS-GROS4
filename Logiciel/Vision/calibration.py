# import picamera
import cv2
import math
import numpy as np
from matplotlib import pyplot as plt
import time

def calib_vision():
    # Fonction permettant de calibrer la caméra sur le robot en fonction
    # des 3 points de repères présent sur la plateforme

    # Prendre une photo:
    # ** SOUS Unix **
    # cap = PiCamera()
    # time.sleep(2)                                 # Attendre que la caméra s'initialise
    # cap.capture("/home/pi/Pictures/img.jpg")
    # print("Photo prise")

    # ** SOUS Windows **
    cap = cv2.VideoCapture(0)

    # Lecture de la photo:
    ret, img = cap.read()

    # Sauvegarder l'image:
    path = r"calibration_pic.jpeg"
    cv2.imwrite(path, img)

    # Conversion de l'image en noir et blanc:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Spécification des valeurs limites (pixel = 0 si < 100 et pixel = 1 si > 255) pour en sortir une image binaire
    _, image_binaire = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

    # Trouver les contours de l'image binaire
    contours, _ = cv2.findContours(image_binaire, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    i = 0
    liste_coord_centres = []

    for c in contours:
        liste_points = []
        perimeter = cv2.arcLength(c,True)

        # Filtrer les perimètres trop petits:
        if perimeter >= 200:
            # Ignorer le premier contour pusique la fonction "findcontour" détecte l'image complète comme premier élément
            if i == 0:
                i = 1
                continue

            # Approximer les formes
            approx = cv2.approxPolyDP(c, 0.01 * cv2.arcLength(c, True), True)

            # Déssiner les contours sur l'image
            cv2.drawContours(img, [c], -1, (0, 255, 0), 2)

            # Trouver le centre des contours
            M = cv2.moments(c)
            if M['m00'] != 0.0:
                x = int(M['m10'] / M['m00'])
                liste_points.append(x)
                y = int(M['m01'] / M['m00'])
                liste_points.append(y)
                liste_coord_centres.append(liste_points)

            # Ajout du texte "Centre" sur l'image au centre des contours
            cv2.putText(img, 'Centre', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        else:
            continue

    plt.imshow(img, cmap="gray")
    plt.show()

    # cv2.imshow('Formes', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Let's say my origin is the up right tape (162, 249):
    # Calculate the distance in X and Y coord. from the origin to the other points:

    # distance_origin_left = [liste_coord_centres[0][0] - liste_coord_centres[1][0], liste_coord_centres[0][1] - liste_coord_centres[1][1]]
    # distance_origin_right = [liste_coord_centres[0][0] - liste_coord_centres[2][0], liste_coord_centres[0][1] - liste_coord_centres[2][1]]

    # Calculate the absolute distance from the origin to the other points:
    # distance_origin_left_absolute = math.sqrt(distance_origin_left[0]**2 + distance_origin_left[1]**2)
    # distance_origin_right_absolute = math.sqrt(distance_origin_right[0]**2 + distance_origin_right[1]**2)

if __name__ == '__main__':
    calib_vision()
