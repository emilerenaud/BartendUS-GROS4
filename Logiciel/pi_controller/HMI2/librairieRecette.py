

class gestion_ingredient_dispo():

    def __init__(self):
        self.list_ingredient = []
        self.list_quantite = []
        self.list_position=[]
        self.path = "pi_controller/HMI2/repertoireIngredient.txt"
        self.lireIngredientDispo()


    def lireIngredientDispo(self):

        f = open(self.path, 'r', encoding="utf-8")
        #exemple typo : Vodka : 750 , position : 8
        for line in f:

            chaine=line.split(",")
            ingredientQuantite=chaine[0].split(":")
            if(len(ingredientQuantite)==2):
                self.list_ingredient.append( ingredientQuantite[0])
                self.list_quantite.append(float(ingredientQuantite[1]))
                textePosition = chaine[1].split(":")
                self.list_position.append(int(textePosition[1]))

        f.close()
        return

    def get_list_ingredient(self):
        return self.list_ingredient

    def get_list_position(self):
        return self.list_position

    def get_list_ingredient_string(self):
        list_chaine=[]
        for i in range(len(self.list_ingredient)):
            chaine =self.list_ingredient[i] + ": " + str(self.list_quantite[i])+" ml, position : "+str(self.list_position[i])
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
        self.supprimerLigneVide()
        chaineAsupprimer=self.list_ingredient[index] + ":" + str(self.list_quantite[index])+", position : "+str(self.list_position[index])
        chaineAsupprimer=chaineAsupprimer.strip('\n')
        f= open(self.path, 'r', encoding="utf-8")
        lines = f.readlines()
        f.close()
        f = open(self.path, 'w', encoding="utf-8")

        for l in range (len(lines)):
            line_actuel=lines[l].strip('\n')
            if line_actuel[0] != chaineAsupprimer[0]:
                f.write(lines[l])
        f.close()

    def supprimerLigneVide(self):
        nbLigneVide=0
        f = open(self.path, 'r', encoding="utf-8")
        lines = f.readlines()
        f.close()
        f = open(self.path, 'w', encoding="utf-8")
        longueur=len(lines)
        l=0
        while l <=longueur-1:
            len(lines) - nbLigneVide - 1
            line_actuel = lines[l+nbLigneVide]
            while lines[l+nbLigneVide]=="\n" and (l+nbLigneVide)<len(lines)-1 :
                nbLigneVide=nbLigneVide+1
                longueur=len(lines)-nbLigneVide-1
            f.write(lines[l+nbLigneVide])
            l=l+1
        f.close()

    def supprimerIngredient(self,index):
        self.supprimerSauvegarde(index)
        self.list_ingredient.pop(index)
        self.list_quantite.pop(index)
        self.list_position.pop(index)
        return


    def sauvegardeIngredient(self, ingredient, quantite, position):
        f = open(self.path, 'a', encoding="utf-8")
        f.write(ingredient + ":" + str(quantite)+", position : "+str(position)+'\n')
        f.close()
        return

    def ajouterIngredient(self, ingredient, quantite, position):

        self.list_ingredient.append(ingredient)
        self.list_quantite.append(quantite)
        self.list_position.append(position)
        self.sauvegardeIngredient(ingredient, quantite, position)
        return

    def isIngredientDoublon(self, ingredient_ajout):
        for ingredient in self.list_ingredient:
            if(ingredient.lower()==ingredient_ajout.lower()):
                return True
        return False

    def isPositionDoublon(self,position_ajout):

        for position in self.list_position:
            if(position==position_ajout):
                return True
        return False

    def update_Quantite(self,index,quantite):
        #self.supprimerLigneVide()
        new_line = self.list_ingredient[index] + ":" + str(self.list_quantite[index]-quantite) + ", position : " + str(self.list_position[index])
        f = open(self.path, 'r', encoding="utf-8")
        lines = f.readlines()
        f.close()
        f = open(self.path, 'w', encoding="utf-8")

        for l in range(len(lines)):
            if l!=index:
                f.write(lines[l])
            else:
                f.write(new_line)
        f.close()



class recette() :

    def __init__(self):
        self.titre = "Swince"
        self.list_alcool = ["swince"]
        self.list_quantite = ["69"]


    def __init__(self,titre, list_alcool,list_quantite):
        self.titre = titre
        self.list_alcool = list_alcool.copy()
        self.list_quantite = list_quantite.copy()
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



class gestion_Recette():

    def __init__(self):
        self.path = "pi_controller/HMI2/repertoireRecette.txt"
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
            list_chaine.append(recette.getTitre())
        return list_chaine

    def list_recette_string(self):
        list_chaine = []
        for recette in self.list_recette:
            list_chaine.append(recette.getTitre())
        return list_chaine

    def getRecette(self,index):
        return self.list_recette[index]

    def sauvegardeRecette(self,recette):
        f = open(self.path, 'a', encoding="utf-8")
        f.write("\n"+recette.__str__())
        f.close()
        return

    def ajouterRecette(self,titre, list_alcool,list_quantite):
        newRecette = recette(titre, list_alcool, list_quantite)
        self.list_recette.append(newRecette)
        self.sauvegardeRecette(newRecette)
        return

    def lireRecette(self):

        f = open(self.path, 'r', encoding="utf-8")
        list_recette=[]

        for line in f:
            list_alcool = []
            list_quantite = []

            recetteIngredient=line.split(",")
            for i in range(1, len(recetteIngredient),1):
               # recetteIngredient[i]=recetteIngredient[i].strip()
                ingredientQuantite=recetteIngredient[i].split(":")
                list_alcool.append(ingredientQuantite[0])
                list_quantite.append(float(ingredientQuantite[1]))
            newRecette=recette(recetteIngredient[0], list_alcool, list_quantite)
            list_recette.append(newRecette)
        f.close()

        return list_recette

    def update_recette_dispo(self,ingredient_dispo):
        list_ingredient=ingredient_dispo.get_list_ingredient()
        list_recette_dispo=[]

        for recette in self.list_recette:
            trouver=0
            nbIngredient=len(recette.getlistAlcool())
            for i in range(nbIngredient):
                if trouver == i:
                    for alcool in list_ingredient:
                        if alcool.lower()==recette.getlistAlcool()[i].lower():
                            if i == nbIngredient-1:
                                list_recette_dispo.append(recette)
                            else:
                                trouver=trouver+1


        self.list_recette_dispo=list_recette_dispo
        return self.list_recette_dispo



    def supprimerSauvegarde(self,index):
        self.supprimerLigneVide()
        chaineAsupprimer=self.list_recette[index].__str__()

        f= open(self.path, 'r', encoding="utf-8")
        lines = f.readlines()
        f.close()
        f = open(self.path, 'w', encoding="utf-8")

        for l in range (len(lines)):
            line_actuel=lines[l].strip('\n')
            if line_actuel != chaineAsupprimer:
                f.write(lines[l])
        f.close()

    def supprimerLigneVide(self):
        nbLigneVide=0
        f = open(self.path, 'r', encoding="utf-8")
        lines = f.readlines()
        f.close()
        f = open(self.path, 'w', encoding="utf-8")
        longueur=len(lines)
        l=0
        while l <=longueur-1:
            pass
            while lines[l+nbLigneVide]=="\n" and (l+nbLigneVide)<len(lines)-1 :
                nbLigneVide=nbLigneVide+1
                longueur=len(lines)-nbLigneVide
            f.write(lines[l+nbLigneVide])
            l=l+1
        f.close()

    def supprimerRecette(self,index):
        self.supprimerSauvegarde(index)
        self.list_recette.pop(index)

        return

# livreIngredient=gestion_ingredient_dispo()
# livreIngredient.update_Quantite(0,3);