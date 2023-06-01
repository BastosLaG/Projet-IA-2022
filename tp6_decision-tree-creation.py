#créer un arbre de décision à partir d'une Base de données (fichier txt)

#désolé, des fois y'a de l'anglais, des fois du français

import math #for log2()
import libs.libAnnexe as lib


name = "" #nom de la BdD (purement décoratif)
filePath = "" #fichier de la BdD
classPos = 0 #position de la classe dans les données (0 = 1er élément)
attributsName = [] #!!! doivent obligatoirement être ordonnés de la même manière que les données
modalitiesToIgnore = [] #tout attributs confondu, afin de ne créer des branches inutiles
treePrintingMod = "" #tab or block, mode d'affichage de l'arbre
createGraph = 0 #est-ce qu'il faut faire un affichage adapté à un fichier .dot (graph)

name, filePath, classPos, attributsName, modalitiesToIgnore, treePrintingMod, createGraph = lib.initGloabals()


class Tree():
    def __init__(self, classe, attributs, datas, entropie, modality, profondeur): #prof est pour le debug, à supprimer
        self.attribut = ("ROOT", []) #nom, modalités
        self.modality = modality #modality m du parent
        self.subTrees = {} #il doit y avoir autant de subTrees que de modalité à "self.attribut" (aka len(self.attribut[1]))

        self.entropie = entropie

        #--- USED FOR DEBUG ---
        # self.attributs = attributs
        # self.datas = datas
        self.profondeur = profondeur #used in self.printTree()
        #----------------------

        self.fillTree(classe, attributs, datas)



    def nbNodes(self):
        if len(self.subTrees) == 0:
            return 1
        
        res = 0

        for subT in self.subTrees.values():
            res += subT.nbNodes()
        
        return 1 + res



    def height(self):
        if len(self.subTrees) == 0:
            return 0
        
        subTreesHeight = []

        for subT in self.subTrees.values():
            subTreesHeight.append(1 + subT.height())

        return lib.greater(subTreesHeight)



    def nbLeaves(self):
        if len(self.subTrees) == 0:
            return 1
        
        res = 0

        for subT in self.subTrees.values():
            res += subT.nbLeaves()

        return res



    def printTreeForPdfContent(self):
        
        for name, subT in self.subTrees.items():
            print(f"\t{self.modality} -> {self.attribut[0]}_{name}")
            subT.printTreeForPdfContent()

    #parcours préfixe
    def printTreeForPDF(self):
        print("digraph G {")
        self.printTreeForPdfContent()
        print("}")






    #parcours préfixe
    #print self.attribut[0] of each node in this format => (root, subtreeL, subtreeR)
    def printTreeWithTab(self):
        print()
        lib.printTab(self.profondeur)

        print(f"{self.modality} : {self.attribut[0]}", end="")

        #si le neoud à des sous arbres...
        if len(self.subTrees) > 0:
            
            i = 0
            for name, subT in self.subTrees.items():
                subT.printTreeWithTab()
                i += 1

                
        
    #parcours préfixe
    #print self.attribut[0] of each node in this format => (root, subtreeL, subtreeR)
    def printTreeOneBlock(self):
        if self.profondeur % 3 == 0:
            print("(", end="")
        elif self.profondeur % 2 == 0:
            print("{", end="")
        else:
            print("[", end="")

        print(f"{self.modality}:{self.attribut[0]}", end="")

        #si le neoud à des sous arbres...
        if len(self.subTrees) > 0:
            print(", ", end="")
            pass
            
            i = 0
            for name, subT in self.subTrees.items():
                subT.printTreeOneBlock()
                i += 1

                if i < len(self.subTrees):
                    print(", ", end="")
                    pass
                
        if self.profondeur % 3 == 0:
            print(")", end="")
        elif self.profondeur % 2 == 0:
            print("}", end="")
        else:
            print("]", end="")



    def printTree(self, mod):
        if mod == "tab":
            self.printTreeWithTab()
        if mod == "block":
            self.printTreeOneBlock()



    def fillTree(self, classe, attributs, datas):

        if len(datas) == 1:
            self.attribut = ("LEAF", [])
            return

        if len(attributs) == 0 or len(datas) == 0: #or len(datas[0]) == 1: #peut-être d'autres if ? ou ajouter d'autres conditions ?
            return


        #=== SMALLEST ENTROPIE =========================
        #trouver l'attribut ayant la plus faible entropie

        smallestEntropie = 1 #greatest value possible

        i = 0
        for att, modalities in attributs.items():
            #si on trouve un attribut avec une entropie null (donc la plus petit valeur possible)
            # if (smallestEntropie == 0):
            #     break

            #si c'est la première boucle du for
            if self.attribut[0] == "ROOT":
                smallestEntropie = entropieBy(self.entropie, classe, modalities, datas, 0)
                self.attribut = (att, modalities)

            else:
                tempEnt = entropieBy(self.entropie, classe, modalities, datas, i)
                
                if (smallestEntropie > tempEnt):
                    smallestEntropie = tempEnt
                    self.attribut = (att, modalities)

            i += 1

        #on va chercher la position de l'att à la plus faible entropie, dans attributs
        index = 0 #index d'un attribut dans "attributs"
        for att, mod in attributs.items():
            if att == self.attribut[0]:
                break
            index += 1
                
        #=== END SMALLEST ENTROPIE =====================


        #=== CREATE SUBTREES ===========================
        self.createSubTrees(classe, attributs, datas, index)
        #=== FIN CREATE SUBTREES =======================

            

    def createSubTrees(self, classe, attributs, datas, index):
        #append autant de Tree() à "self.subTrees" qu'il y'a de modalités à "self.attribut"

        #pour chaque modalité de "self.attribut"
        for modality in self.attribut[1]:
            if modality in modalitiesToIgnore:
                continue

            newAtts = attributs.copy()
            newEts = [] #on va append une copy de chaques n de "datas" (sinon, les éléments de "datas" seront modifiés, et on ne veux pas)

            for n in datas:
                newEts.append(n.copy())


            #on retire les datas qui n'ont pas la bonne modalité
            #ou la valeur à la position correspondant à l'attribut
            j = 0 #index dans la liste des états (newEts)
            #rappel : index = index d'un attribut dans le dico des attributs (attributs)
            
            while j < len(newEts):

                #on retire l'état de la liste
                if not newEts[j][index] == modality:
                    newEts.pop(j)
                
                else:
                    j += 1
                

            #on retire la valeur de chaque état à l'indice correspondant à la position de l'attribut dans "attributs"
            for e in newEts:
                e.pop(index)

            #on retire l'attribut de la liste
            newAtts.pop(self.attribut[0])

            #on ajoute un subTree, en lui donnant les attributs et états restants
            if (len(newEts) > 0 and len(newAtts) > 0):
                subTreeModality = self.attribut[0] + "=" + modality
                self.subTrees[subTreeModality] = Tree(classe, newAtts, newEts, self.entropie, subTreeModality, self.profondeur + 1)
                
            else:
                return





#la somme, pour chaque modalité (k) de la classe, de la proba de Ai sachant k * log2 de la proba de Ai sachant Ck
def shannonSommeCSachantAi(classe, Ai, datas, index, numerateurAi):
    somme = 0

    for k in classe[1]:
        nbAiCk = 0 #nb d'apparition d'une modalité, sachant la modalité de la classe
        for e in datas:
            if e[-1] == k and e[index] == Ai:
                nbAiCk += 1

        prob = nbAiCk / numerateurAi
        if prob == 0:
            # continue
            return 0
            
        somme += prob * math.log2(prob)
    
    return somme




#la somme, pour chaque modalité (k) de la classe (C), de la proba de Ai sachant Ck au carré
def giniSommeCSachantAi(classe, Ai, datas, index, numerateurAi): #name ici juste pour le débug, à retirer
    somme = 0


    for k in classe[1]:
        nbAiCk = 0 #nb d'apparition d'une modalité, sachant la modalité de la classe
        for e in datas:
            if e[-1] == k and e[index] == Ai:
                nbAiCk += 1


        somme += (nbAiCk / numerateurAi) ** 2
    
    return somme
    

#attribut:list des mod d'un attribut, index = position de l'attribut dans "attributs"
def entropieBy(byUsingThat, classe, attribut, datas, index):
    res = 0
    denomi = len(datas)

    for i in attribut: #i est une modalité de l'attribut
        #on compte dans combien d'états est "i"
        nbAi = 0 #proba d'une modalité
        for e in datas:
            if e[index] == i:
                nbAi += 1

        if nbAi == 0:
            pass
        else:
            if byUsingThat == "gini":
                res += (nbAi / denomi) * (1 - giniSommeCSachantAi(classe, i, datas, index, nbAi))
            if byUsingThat == "shannon":
                res += -1 * ((nbAi / denomi) * shannonSommeCSachantAi(classe, i, datas, index, nbAi))

    return res

    








 












def main():
    global filePath
    global classPos
    global attributsName
    global createGraph

    datasInit = [] #liste des données (une donnée étant une liste de str)
    attributsInit = {} #attributs de la classe ("name": [modalities])
    classeInit = () #classe of datas ("name", [modalities])

    #=== INITIALISATION ==========================
    datasInit = lib.extractDataFromFile(filePath)


    attributsInit = lib.determineAttributsFromData(datasInit, attributsName)

    #on retire la classe de la liste, qu'on va isoler
    for key, val in attributsInit.items():
        if key == attributsName[classPos]:
            classeInit = (key, val)
            attributsInit.pop(key)
            break

    #on retire les modalités interdites
    for key, val in attributsInit.items():
        i = 0
        while 1:
            if i == len(val):
                break

            if val[i] in modalitiesToIgnore:
                val.pop(i)
                continue

            i += 1


    #pour chaque données, on place la valeur correspondant à la classe en fin de liste
    if not classPos >= len(datasInit[0]) - 1:
        for n in datasInit:
            x = n.pop(classPos)
            n.append(x)

    #=== FIN INITIALISATION ======================


    # classeInit = ("jd", ["0", "1"])
    # attributsInit = {"df": ["0", "1"],
    #                  "bh": ["0", "1"],
    #                  "bt": ["0", "1"],
    #                  "gp": ["0", "1"]}

    # #df = devoirs fait, bh = bonne humeur des parent, bt = beau temps, gp = gouter pris, jd = jouer dehors
    # #JD est la classe
    # #             [df,  bh , bt,  gp,  JD]
    # datasInit = [["1", "0", "1", "0", "1"],
    #              ["0", "1", "0", "1", "1"],
    #              ["1", "1", "1", "0", "1"],
    #              ["1", "0", "1", "1", "1"],
    #              ["0", "1", "1", "1", "0"],
    #              ["0", "1", "0", "0", "0"],
    #              ["1", "0", "0", "1", "0"],
    #              ["1", "1", "0", "0", "0"]]


    #arg4 = n in ["gini", "shannon"]
    treeGini = Tree(classeInit, attributsInit, datasInit, "gini", "ROOT", 0)
    treeShannon = Tree(classeInit, attributsInit, datasInit, "shannon", "ROOT", 0)



    if (createGraph):
        treeGini.printTreeForPDF()
        return

    if treeGini.nbNodes() < treeShannon.nbNodes():
        treeGini.printTree(treePrintingMod)
        print("\nGini Tree Printed")
    else:
        treeShannon.printTree(treePrintingMod)
        print("\nShannon Tree Printed")

    print()
    print(f"Database : {name}\n")

    print("Tree create with Gini :")
    print(f"nbNodes={treeGini.nbNodes()}, height={treeGini.height()}, nbLeaves={treeGini.nbLeaves()}")

    print()
    print("Tree create with Shannon :")
    print(f"nbNodes={treeShannon.nbNodes()}, height={treeShannon.height()}, nbLeaves={treeShannon.nbLeaves()}")



if __name__=="__main__":
    main()



#"jouer dehors" datas
"""

    classeInit = ("jd", ["0", "1"])
    attributsInit = {"df": ["0", "1"],
                     "bh": ["0", "1"],
                     "bt": ["0", "1"],
                     "gp": ["0", "1"]}

    #df = devoirs fait, bh = bonne humeur des parent, bt = beau temps, gp = gouter pris, jd = jouer dehors
    #JD est la classe
    #             [df,  bh , bt,  gp,  JD]
    datasInit = [["1", "0", "1", "0", "1"],
                 ["0", "1", "0", "1", "1"],
                 ["1", "1", "1", "0", "1"],
                 ["1", "0", "1", "1", "1"],
                 ["0", "1", "1", "1", "0"],
                 ["0", "1", "0", "0", "0"],
                 ["1", "0", "0", "1", "0"],
                 ["1", "1", "0", "0", "0"]]


(ROOT:bt,
    [bt=0:df,
        {df=0:gp,
            (gp=0:LEAF),
            (gp=1:LEAF)},
        {df=1:bh,
            (bh=0:LEAF),
            (bh=1:LEAF)}],
    [bt=1:df,
        {df=0:LEAF},
        {df=1:bh,
            (bh=0:gp),
            (bh=1:LEAF)}])

"""
