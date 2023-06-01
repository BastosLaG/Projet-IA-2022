
def initGloabals():
    name = ""
    filePath = ""
    classPos = 0
    attributsName = []
    modalitiesToIgnore = []
    treePrintingMod = ""
    createGraph = 0
    i = 1
    
    #dataBaseInfo.txt est relatif au programme appelant cette lib
    with open('dataBaseInfo.txt', 'rt') as file:
        for line in file:
            if i == 1: #name
                data = ""
                for char in line:
                    if char == '\n':
                        name = data
                        break
                    data += char
            elif i == 2: #filePath
                data = ""
                for char in line:
                    if char == '\n':
                        filePath = data
                        break
                    data += char
            elif i == 3: #classPos
                data = ""
                for char in line:
                    if char == '\n':
                        classPos = int(data)
                        break
                    data += char
            elif i == 4: #attributsName
                data = ""
                for char in line:
                    if char == '\n':
                        attributsName.append(data)
                        break
                    if char == ',':
                        attributsName.append(data)
                        data = ""
                        continue
                    data += char
            elif i == 5: #modalitiesToIgnore
                data = ""
                for char in line:
                    if char == '\n':
                        modalitiesToIgnore.append(data)
                        break
                    if char == ',':
                        modalitiesToIgnore.append(data)
                        data = ""
                        continue
                    data += char
            elif i == 6: #treePrintingMod
                data = ""
                for char in line:
                    if char == '\n':
                        treePrintingMod = data
                        break
                    data += char
            elif i == 7: #createGraph
                data = ""
                for char in line:
                    if char == '\n':
                        createGraph = int(data)
                        break
                    data += char
            else:
                break
            i += 1
        
    return name, filePath, classPos, attributsName, modalitiesToIgnore, treePrintingMod, createGraph





#lit un fichier de données, pour retourne chacune d'elle dans un dictionnaire
def extractDataFromFile(path):
    # global dataToIgnore
    datas = []
    data = []

    with open(path, 'rt') as file:
        for line in file:
            dataElement = "" #correspond à une modalité d'un attribut
            for char in line:
                if char == '\n':
                    data.append(dataElement)
                    break

                # if char in dataToIgnore:
                #     continue

                if char == ',':
                    data.append(dataElement)
                    dataElement = ""
                    continue

                dataElement += char

            datas.append(data.copy())
            data.clear()

    return datas






#on retourne un dictionnaire contenant chaque attribut de la classe avec leurs modalités
def determineAttributsFromData(datas, attName):
    nbAtt = len(datas[0])
    tempAtt = {}

    #on initialise des emplacement vide dans le dict
    for i in range(nbAtt):
        tempAtt[i] = []


    #on remplis le dico
    for data in datas:
        for i in range(nbAtt):
            if not data[i] in tempAtt[i]:
                tempAtt[i].append(data[i])


    #on renomme les clés du dict
    attributs = {}
    i = 0
    for key in tempAtt.keys():
        attributs[attName[i]] = tempAtt[key].copy()
        i += 1

    return attributs
    





def printTab(x):
    if x == 0:
        return
    print("    ", end="")
    printTab(x-1)


def greater(list):
    res = list[0]

    for n in list:
        if n > res:
            res = n

    return res
