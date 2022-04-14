import cv2
from matplotlib import pyplot as plt

class Calibration_cam():
    # Classe permettant de calibrer la caméra sur le robot en fonction
    # des 3 points de repères présents sur la plateforme


    def __init__(self):
        self.liste_coord_centres_ref = []
        self.liste_points_coord_centre = []
        self.seuil = 25
        self.get_data_from_reference()      # Appel de la fonction pour aller chercher les datas de l'image de référence


    def get_data_from_reference(self):
        """
        Fonction permettant d'aller chercher les centres des points de référence sur l'image de référence.
        L'image de référence doit être prise avant, lorsque la position de la caméra est parfaite (un bout de code
        dans le main permet de prendre une photo et la sauvegarder dans le même dossier).
        """

        print("Commencement get_data_from_reference()")
        # path = "Vision/img_reference_calib.png"               # Si on roule avec le HMI
        #path = "img_reference_calib.png"                       # Si on roule juste calibration.py
        # path = "/home/pi/Pictures/img_reference_calib.png"  # Pour le Pi
        # path = "pic_8.jpeg"
        path = "Vision/pic_8.jpeg"

        img_reference = cv2.imread(path)

        # Conversion de l'image en noir et blanc:
        gray = cv2.cvtColor(img_reference, cv2.COLOR_BGR2GRAY)

        # plt.imshow(gray, cmap="gray")
        # plt.show()
        #
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # Spécification des valeurs limites (pixel = 0 si < 100 et pixel = 1 si > 255) pour en sortir une image binaire
        _, image_binaire = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

        # plt.imshow(image_binaire, cmap="gray")
        # plt.show()

        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # Trouver les contours de l'image binaire
        contours, _ = cv2.findContours(image_binaire, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        i = 0
        for c in contours:
            liste_points_ref = []
            perimeter = cv2.arcLength(c, True)
            area = cv2.contourArea(c, True)

            # print(perimeter)
            # print(area)

            # Filtrer les perimètres trop petits:
            # if area <= -500:
            if 53 <= perimeter <= 70:
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
                    # print(liste_points_ref)

                    if liste_points_ref[0] != 1 and liste_points_ref[0] != 368 and liste_points_ref[0] != 150:
                        self.liste_coord_centres_ref.append(liste_points_ref)
                        cv2.circle(img_reference, (x, y), radius=3, color=(0, 0, 255), thickness=-1)
            else:
                continue
        print(self.liste_coord_centres_ref)
        # plt.imshow(img_reference, cmap="gray")
        # plt.show()
        #
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()



    def calib_vision_init(self):
        """
        Fonction permettant d'ouvrir une fenêtre affichant ce que la caméra voit en temps réel. De plus
        elle affiche 3 points sur cette fenêtre correspondant à la position des centres des trois repères.

        De cette façon, l'utilisateur peut bouger physiquement la caméra pour superposer ces 3 points aux centres
        des points de références réel sur la plateforme pour recalibrer la caméra.
        """

        print("Commencement calib_vision_init()")

        cv2.namedWindow("Calibration - Appuyer sur ESC pour fermer la fenêtre", 1)   #cv2.WINDOW_NORMAL
        cap = cv2.VideoCapture(0)       # Identifier le bon port de caméra -> 0 si pas d'autres caméra (plupart des cas) et 1 sinon

        # Vérifier que l'ouverture de la caméra se fait correctement:
        if cap.isOpened():
            rval, img_reel_time = cap.read()
        else:
            rval = False
            print("ERREUR - Ne peut pas ouvrir la caméra!")

        # Affichage des 3 points sur l'HMI (Fermeture de la fenêtre avec la touche "ESC" (Raspberry Pi et Windows) ou le "X" de la fenêtre qui s'ouvre (Windows seulement))
        while rval and cv2.getWindowProperty("Calibration", cv2.WND_PROP_VISIBLE):
            for center in self.liste_coord_centres_ref:
                cv2.circle(img_reel_time, (center[0], center[1]), radius = 3, color = (0, 0, 255), thickness = -1)

            # Pour afficher l'image en plein écran :
            # cv2.setWindowProperty("Calibration", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.imshow("Calibration", img_reel_time)
            rval, img_reel_time = cap.read()

            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break

        cv2.destroyAllWindows()
        cap.release()



    def calib_vision_seuil(self):
        '''
        Fonction permettant de vérifier si la caméra est décalibré par rapport aux trois points de référence et d'un seuil défini.
        Return True si la caméra est bien calibrée
        Return False si la caméra est décalibrée
        '''

        print("Commencement calib_vision_seuil()")

        # Prendre une photo:
        # cv2.namedWindow("Calibration_seuil")
        cap = cv2.VideoCapture(0)

        if cap.isOpened():
            rval, img_to_verify = cap.read()
        else:
            rval = False
            print("ERREUR - Ne peut pas ouvrir la caméra!")

        # Conversion de l'image en noir et blanc:
        gray = cv2.cvtColor(img_to_verify, cv2.COLOR_BGR2GRAY)

        # Spécification des valeurs limites (pixel = 0 si < 100 et pixel = 1 si > 255) pour en sortir une image binaire
        _, image_binaire = cv2.threshold(gray, 192, 255, cv2.THRESH_BINARY)

        plt.imshow(image_binaire, cmap="gray")
        plt.show()

        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Trouver les contours de l'image binaire
        contours, _ = cv2.findContours(image_binaire, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        i = 0
        for c in contours:
            liste_points_verify = []
            perimeter = cv2.arcLength(c, True)
            area = cv2.contourArea(c, True)

            # print(perimeter)
            # print(area)

            # Filtrer les perimètres trop petits:
            # if area <= -500:
            if 53 <= perimeter <= 70:
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
                    x1 = int(M['m10'] / M['m00'])
                    liste_points_verify.append(x1)
                    y1 = int(M['m01'] / M['m00'])
                    liste_points_verify.append(y1)

                    if liste_points_verify[0] != 1 and liste_points_verify[0] != 368 and liste_points_verify[0] != 150:
                        self.liste_points_coord_centre.append(liste_points_verify)
                        cv2.circle(img_to_verify, (x1, y1), radius=3, color=(0, 0, 255), thickness=-1)
            else:
                continue
        print("Centre photo seuil : \n")
        print(self.liste_points_coord_centre)

        plt.imshow(img_to_verify, cmap="gray")
        plt.show()

        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Vérification si les centre respectent le seuil ou non par rapport à l'image de référence
        for point in range(len(self.liste_points_coord_centre)):

            # Détecter si le seuil est bon selon X:
            if not (self.liste_coord_centres_ref[point][0] - self.seuil <= self.liste_points_coord_centre[point][0] <= self.liste_coord_centres_ref[point][0] + self.seuil):
                print("CALIBRATION NÉCESSAIRE: Coordonnée en X ne respecte pas le seuil")
                return False

            # Détecter si le seuil est bon selon Y:
            elif not (self.liste_coord_centres_ref[point][1] - self.seuil <= self.liste_points_coord_centre[point][1] <= self.liste_coord_centres_ref[point][1] + self.seuil):
                print("CALIBRATION NÉCESSAIRE: Coordonnée en Y ne respecte pas le seuil")
                return False

        return True



if __name__ == '__main__':
    # path = r"pic_8.jpeg"
    # cap = cv2.VideoCapture(0)

    # # Check if the webcam is opened correctly
    # if not cap.isOpened():
    #     raise IOError("Cannot open webcam")
    # ret, img = cap.read()
    # cv2.imwrite(path, img)

    calib = Calibration_cam()
    # calib.calib_vision_init()
    calib.calib_vision_seuil()

    #calib.calib_vision_seuil()
    # calib_vision_seuil()
    # calib.calib_vision_init
    print('Done with vision')
