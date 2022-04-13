class ingredient_dispo():


    def __init__(self):
        self.list_ingredient = []
        self.list_quantite = []
        self.list_position=[]
        self.lireIngredientDispo()

    def lireIngredientDispo(self):

        f = open("repertoireIngredient.txt", 'r', encoding="utf-8")
        #exemple typo : Vodka : 750 , position : 8
        for line in f:

            chaine=line.split(",")
            ingredientQuantite=chaine[0].split(":")
            self.list_ingredient.append( ingredientQuantite[0])
            self.list_quantite.append( ingredientQuantite[1])

            textePosition = chaine[1].split(":")
            self.list_position.append(textePosition[1])

        f.close()
        return

    def get_list_ingredient(self):
        return self.list_ingredient

    def get_list_ingredient_string(self):
        list_chaine=[]
        for i in range(len(self.list_ingredient)):
            chaine =self.list_alcool[i] + ":" + str(self.list_quantite[i]+"ml position : "+str(self.list_position[i]))
            list_chaine.append(chaine)
        return list_chaine

    def __str__(self):
        chaine=""
        for i in range(len(self.list_ingredient)):
                chaine =chaine+ self.list_ingredient[i] + ":" + str(self.list_quantite[i]) + "ml, Position:" + str(self.list_position[i])
                if chaine[-1]!="\n":
                    chaine=chaine+"\n"
        return chaine

    def supprimerSauvegarde(self,index):
        chaineAsupprimer=self.list_ingredient[index] + ":" + str(self.list_quantite[index])+", position : "+str(self.list_position[index])
        f= open("repertoireIngredient.txt", 'r', encoding="utf-8")
        lines = f.readlines()
        f = open("repertoireIngredient.txt", 'w', encoding="utf-8")
        for line in lines:
            if line.strip("\n") != chaineAsupprimer:
                f.write(line)

    def supprimerIngredient(self,index):
        self.supprimerSauvegarde(index)
        self.list_ingredient.pop(index)
        self.list_quantite.pop(index)
        self.list_position.pop(index)
        return


    def sauvegardeIngredient(self, ingredient, quantite, position):
        f = open("repertoireIngredient.txt", 'a', encoding="utf-8")
        f.write("\n"+ingredient + ":" + str(quantite)+", position : "+str(position))
        f.close()
        return

    def ajouterIngredient(self, ingredient, quantite, position):

        self.list_ingredient.append(ingredient)
        self.list_quantite.append(quantite)
        self.list_position.append(position)
        self.sauvegardeIngredient(ingredient, quantite, position)
        return






class recette() :

    def __init__(self):
        self.titre = "Swince"
        self.list_alcool = ["swince"]
        self.list_quantite = ["69"]

    def __init__(self,titre, list_alcool,list_quantite):
        self.titre = titre
        self.list_alcool = list_alcool
        self.list_quantite = list_quantite
        return

    def getTitre(self):
        return self.titre

    def getlistAlcool(self):
        return self.list_alcool

    def getlistQuantite(self):
        return self.list_quantite

    def afficherIngredient(self):
        chaine = ""
        for i in range(len(self.list_alcool)):
            chaine = chaine +str(i+1)+". " + self.list_alcool[i] + ", Quantité:" + str(self.list_quantite[i])+"oz \n"
        return chaine

    def __str__(self):
        chaine=self.titre
        for i in range(len(self.list_alcool)):
            chaine=chaine+"," + self.list_alcool[i] + ":" + str(self.list_quantite[i])
        return chaine



class livreRecette():

    def __init__(self):
        self.list_recette=self.lireRecette()
        self.list_recette_dispo=[]
        return

    def __str__(self):
        chaine=""
        for recette in self.list_recette:
            chaine=""+chaine+recette.__str__()+"\n"
        return chaine

    def afficherRecetteDispo(self):
        chaine = ""
        for recette in self.list_recette_dispo:
            chaine = "" + chaine + recette.__str__() + "\n"
        return chaine

    def list_recette_dispo_string(self):
        list_chaine = []
        for recette in self.list_recette_dispo:
            list_chaine.append(recette.getTitre)
        return list_chaine

    def getRecette(self,index):
        return self.list_recette[index]

    def sauvegardeRecette(self,recette):
        f = open("repertoireRecette.txt", 'a', encoding="utf-8")
        f.write("\n"+recette.__str__())
        f.close()
        return

    def ajouterRecette(self,titre, list_alcool,list_quantite):
        newRecette = recette(titre, list_alcool, list_quantite)
        self.list_recette.append(newRecette)
        self.sauvegardeRecette(newRecette)
        return

    def lireRecette(self):

        f = open("repertoireRecette.txt", 'r', encoding="utf-8")
        list_recette=[]

        for line in f:
            list_alcool = []
            list_quantite = []

            recetteIngredient=line.split(",")
            for i in range(1, len(recetteIngredient),1):
               # recetteIngredient[i]=recetteIngredient[i].strip()
                ingredientQuantite=recetteIngredient[i].split(":")
                list_alcool.append(ingredientQuantite[0])
                list_quantite.append(int(ingredientQuantite[1]))
            newRecette=recette(recetteIngredient[0], list_alcool, list_quantite)
            list_recette.append(newRecette)
        f.close()

        return list_recette

    def update_recette_dispo(self,ingredient_dispo):
    #TO DO
    # GERER LOWER CASE
        list_ingredient=ingredient_dispo.get_list_ingredient()
        list_recette_dispo=[]

        for recette in self.list_recette:
            trouver=0
            nbIngredient=len(recette.getlistAlcool())
            for i in range(nbIngredient):
                if trouver == i:
                    for alcool in list_ingredient:
                        if alcool==recette.getlistAlcool()[i]:
                            if i == nbIngredient-1:
                                list_recette_dispo.append(recette)
                            else:
                                trouver=trouver+1


        self.list_recette_dispo=list_recette_dispo
        return self.list_recette_dispo

##test
livreIngredient=ingredient_dispo()
# print(livreIngredient.list_ingredient[1])
# print("recette dispo :",livreIngredient)
# livreIngredient.supprimerIngredient(2)
# print("recette dispo :",livreIngredient)
#init livre
livre=livreRecette()
# print(livre)
livre.update_recette_dispo(livreIngredient)
# print(livre.list_recette_dispo[0].afficherIngredient())
livreIngredient.ajouterIngredient("rhum",2,1)
livreIngredient.ajouterIngredient("cola",2,1)
print("livreIngredient : \n",livreIngredient)
livre.ajouterRecette("bloodyhell",["bloody","tequila"],[6,9])

print(livre)
# print("La/les recette(s) disponible(s) sont : \n",livre.afficherRecetteDispo())



#
# def wait_for_done():
#     time.sleep(0.5)
#     messageIn = arduino.readline()
#     if(messageIn)
#
#     return data
#
# def send_message(x):
#     arduino.write(bytes(x, 'utf-8'))
#     time.sleep(0.5)
#     data = arduino.readline()
#     return data
#
# # en deg
# def poignet(angle):
#     position = "G4:A" + str(angle) + "\r\n"
#     value = send_message(position)
#     if wait_for_done()is False:
#         wait_for_done()
#
#
#     return
#
# def servo(angle):
#     position = "G5:A" + str(angle) + "\r\n"
#     value = send_message(position)
#     return
#
# def electro(activate):
#     if activate:
#         position = "M1" + "\r\n"
#         value = send_message(position)
#     else:
#         position = "M0" + "\r\n"
#         value = send_message(position)
#     return
#
#     # z est en mm
#
# def moveUpDown(z):
#     position = "G3:Z" + str(z) + "\r\n"
#     value = send_message(position)
#     return
#
# def moveTo(x, y):
#     r.inverseKinematic(x, y)
#     angles = r.getAngleDeg()
#     position = "G0:A" + str(angles[0]) + ":B" + str(angles[1]) + "\r\n"
#     value = send_message(position)
#     return
#
#
#
# def homing():
#     # caller la fonction HOME
#     homing = "G2\r\n"
#     send_message(homing)
#     return
#
# def versement():
#     poignet(120)
#     moveUpDown(20)
#
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
#
#




