

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


    def getRecette(self,index):
        return self.list_recette[index]

    def sauvegardeRecette(self,recette):
        f = open("repertoireRecette.txt", 'a', encoding="utf-8")
        f.write(recette.__str__())
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
        # debut=False
        # while(debut is not True):
        #     if(f.read() != 'G'):
        #         debut=True
        #         print("go")
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

    def update_recette_dispo(self,list_alcool):
        list_recette_dispo=[]

        for recette in self.list_recette:
            trouver=0
            nbIngredient=len(recette.getlistAlcool())
            for i in range(nbIngredient):
                if trouver == i:
                    for alcool in list_alcool:
                        if alcool==recette.getlistAlcool()[i]:
                            if i == nbIngredient-1:
                                list_recette_dispo.append(recette)
                            else:
                                trouver=trouver+1


        self.list_recette_dispo=list_recette_dispo
        return self.list_recette_dispo

##test
list_alcool=["alcool","alcool2","lime","swince"]
#init livre
livre=livreRecette()
print(livre)
livre.update_recette_dispo(list_alcool)
print("La/les recette(s) disponible(s) sont : \n",livre.afficherRecetteDispo())





