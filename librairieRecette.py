

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

    def __str__(self):
        chaine=self.titre
        for i in range(len(self.list_alcool)):
            chaine=chaine+"," + self.list_alcool[i] + ":" + self.list_quantite[i]
        return chaine



class livreRecette():

    def __init__(self):
        self.list_recette=self.lireRecette()
        self.list_recette_dispo=[]

    def getRecette(self,index):
        return self.list_recette[index]

    def sauvegardeRecette(self,recette):
        f = open("repertoireRecette.txt", 'a', encoding="utf-8")
        f.write(self.__str__())
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
            recetteIngredient=f.readline().split(",")
            for i in range(1, len(recetteIngredient)):
                ingredientQuantite=recetteIngredient[i].split(":")
                list_alcool.append(ingredientQuantite[0])
                list_quantite.append(ingredientQuantite[1])
            newRecette=recette(recetteIngredient[0], list_alcool, list_quantite)
            list_recette.append(newRecette)
        f.close()

        return len(list_recette)

    def list_recette_dispo(self,list_alcool):

        list_recette_dispo=[]
        # for recette in self.list_recette:
        #     for alcool in list_alcool:
        #         for ingredient in recette.getlistAlcool():
        #             if ingredient==alcool:
        #                 present=True
        #                 break

        self.list_recette_dispo=list_recette_dispo
        return self.list_recette_dispo






