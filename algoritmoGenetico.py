import random
import math
import pandas as pd

def poblacionInicial(tamPoblacion): # Crea una poblacion inicial random
    cromosomas = []
    for i in range(tamPoblacion):
        entero = random.randint(0, 15)
        cadBinaria = "{0:04b}".format(entero)
        cromosomas.append(cadBinaria)

    return cromosomas

def funcionObjetivo(x):
    resultado = abs((x - 5) / (2 + math.sin(x)))
    return resultado

def decodificarCromosomas(cromosomas):
    cromosomasDecodificado = []
    for gen in cromosomas:
        cromosomasDecodificado.append(int(gen, 2)) 

    return cromosomasDecodificado

def decodificarCromosoma(cromosoma):
    cromosomaDecodificado = int(cromosoma, 2) 
    return cromosomaDecodificado

def seleccionPadre(valor): # Funcion que selecciona a un padre por el metodo de la ruleta 
    diferencias = []

    # Calculamos la diferencia entre el valor random y la 
    # probabilidad de seleccion acumulada de cada cromosoma o individuo decodificado (fenotipo)
    for individuo in pSelAcumulada:
        diferencia = abs(individuo - valor)
        diferencias.append(diferencia)

    padreSeleccionado = diferencias.index(min(diferencias)) # Obtiene el individuo o padre
    return padreSeleccionado

# Funcion para hacer la cruza
def cruzaUniforme(padre1, padre2):
    randoms = [] # Arreglo con numeros random del tamaño de los cromosomas 
    hijo1 = []
    hijo2 = []
    cruza = random.uniform(0, 1) # Numero aleatorio para definir si hay cruza o no  
    umbral = 0.5 # Umbral para definir de que padre se toma el gen del hijo 

    if cruza > pC: # No hay cruza
        # print("\nNo hubo cruza\n")
        individuo1 = padre1
        individuo2 = padre2
        hijo1 = individuo1
        hijo2 = individuo2
    else:
        # print("Hubo cruza")
        for i in range(tamCromosoma):
            numRandom = random.uniform(0, 1)
            randoms.append(numRandom)
        # print("\nNumeros random\n", randoms, "\n")

        i = 0
        for numRandom in randoms:
            if numRandom <= umbral:
                hijo1.append(padre1[i])
                hijo2.append(padre2[i])
            else:
                hijo1.append(padre2[i])
                hijo2.append(padre1[i])

            i += 1

        # print("\nEtapa mutacion")
        # print("\nHijo1 antes de ser mutado", hijo1)
        # print("Hijo2 antes de ser mutado", hijo2, "\n")

        hijo1 = mutarIndividuo(hijo1, 1)
        hijo2 = mutarIndividuo(hijo2, 2)

        hijo1 = ''.join(hijo1)
        hijo2 = ''.join(hijo2)

        # print("\nEtapa sobrevivietes")
        hijo1, hijo2 = remplazarMasDebil(padre1, padre2, hijo1, hijo2)
    
    return hijo1, hijo2

def mutarIndividuo(individuo, numHijo):
    randoms = [] # Arreglo con numeros random del tamaño de los cromosomas 
    hijo = []

    for i in range(tamCromosoma):
        numRandom = random.uniform(0, 1)
        randoms.append(numRandom)
    # print("\nNumeros random\n", randoms, "\n")

    i = 0
    for numRandom in randoms:
        if numRandom <= pM:
            # print("Muto gen: ", i, "del individuo", numHijo)
            if individuo[i] == '0':
                hijo.append('1')
            elif individuo[i] == '1':
                hijo.append('0')
        else:
            hijo.append(individuo[i])

        i += 1
    
    return hijo

def remplazarMasDebil(padre1, padre2, hijo1, hijo2):
    mejoresIndividuos = []
    valoresAptitud = []
    valorpadre1 = decodificarCromosoma(padre1)
    valorpadre2 = decodificarCromosoma(padre2)
    hijo1 = decodificarCromosoma(hijo1)
    hijo2 = decodificarCromosoma(hijo2)
    fenotiposIndividuos = [valorpadre1, valorpadre2, hijo1, hijo2]

    # print("\nFenotipos individuos\n", fenotiposIndividuos)

    for cromosoma in fenotiposIndividuos:
        valoresAptitud.append(funcionObjetivo(cromosoma))
    # print("\nValores aptitud\n", valoresAptitud, "\n")

    for i in range(2):
        mejorIndividuo = valoresAptitud.index(max(valoresAptitud))
        mejoresIndividuos.append(fenotiposIndividuos[mejorIndividuo])
        fenotiposIndividuos.pop(mejorIndividuo)
        valoresAptitud.pop(mejorIndividuo)
    # print("Fenotipos mejores individuos", mejoresIndividuos, "\n")

    individuo1 = "{0:04b}".format(mejoresIndividuos[0])
    individuo2 = "{0:04b}".format(mejoresIndividuos[1])

    return individuo1, individuo2
        
# cromosomas = []
# cromosomasDecodificado = []
# valoresAptitud = []
# pSel = [] # Probabilidad seleccion 
# pSelAcumulada = []  # Probabilidad seleccion acumulada
# newPoblacion = []
# totalValoresAptitud = 0
# totalValorespSel = 0
tamPoblacion = 10
numGeneracionesMaximo = 10
pC = 0.853 # Probabilidad cruza
pM = 0.1 # Probabilidad mutacion

numBinario = "{0:b}".format(15) # Valor maximo de x
tamCromosoma = len(numBinario)
# print("Tamaño cromosoma: ",tamCromosoma, "\n")

newPoblacion = poblacionInicial(tamPoblacion) # Creamos la poblacion inicial 
# print("Poblacion inicial\n", cromosomas)

for generacion in range(numGeneracionesMaximo + 1):
    cromosomas = newPoblacion
    cromosomasDecodificado = []
    valoresAptitud = []
    pSel = [] # Probabilidad seleccion 
    pSelAcumulada = []  # Probabilidad seleccion acumulada
    newPoblacion = []
    totalValoresAptitud = 0
    totalValorespSel = 0

    print("\nGeneracion: ", generacion)
    # print("\nCromosomas\n", cromosomas)

    cromosomasDecodificado = decodificarCromosomas(cromosomas) # Decodificamos los cromosomas (obtenemos el fenotipo)
    # print("\nFenotipo\n", cromosomasDecodificado)

    # Valores aptitud
    for genDecodificado in cromosomasDecodificado:
        resultado = funcionObjetivo(genDecodificado) # Evaluamos el fenotipo en la funcion objetivo para obtener su valor de aptitud
        valoresAptitud.append(resultado)
    # print("\nValores aptitud\n", valoresAptitud)

    # Total valor aptitud
    for valor in valoresAptitud:
        totalValoresAptitud += valor

    # print("\nTotal valor aptitud\n", totalValoresAptitud)

    # Valores de probabilidad de seleccion S
    for valor in valoresAptitud:
        pSel.append(valor / totalValoresAptitud)
    # print("\npSel\n", pSel)

    # Total de probabilidad de seleccion y Probabilidad de seleccion acumulada
    for VpSel in pSel:
        totalValorespSel += VpSel
        pSelAcumulada.append(totalValorespSel)
    # print("\nTotal probabilidad de seleccion\n", totalValorespSel)
    # print("\nPSelAcumulada\n", pSelAcumulada)
    
    index = ["Individuo1", "Individuo2", "Individuo3", "Individuo4", "Individuo5",
             "Individuo6", "Individuo7", "Individuo8", "Individuo8", "Individuo10"]
    tablaDatos = list(zip(cromosomas, cromosomasDecodificado, valoresAptitud, pSel, pSelAcumulada))
    df = pd.DataFrame(tablaDatos, columns=["Cromosomas", "Fenotipo", "ValorAptitud", "pSel", "pSelAcumulada"], index=index)
    print(df, "\n")

    for i in range(int(tamPoblacion / 2)):
        # print("\nEtapa seleccion padres\n")
        # Busca valores aleatorios para escoger a los padres
        Aleatorio1 = random.uniform(0, 1)
        Aleatorio2 = random.uniform(0, 1)

        # print("\nAleatorio1: ", Aleatorio1)
        # print("Aleatorio2: ", Aleatorio2, "\n")

        padre1Index = seleccionPadre(Aleatorio1) # Selecciona padre1
        padreAnterior = padre1Index
        padre2Index = seleccionPadre(Aleatorio2) # Selecciona padre2
        while(padre2Index == padreAnterior):
            Aleatorio2 = random.uniform(0, 1)
            padre2Index = seleccionPadre(Aleatorio2) # Selecciona un nuevo padre si los padres seleccionados son iguales

        # Padres seleccionados
        padre1 = cromosomas[padre1Index]
        padre2 = cromosomas[padre2Index]

        # print("\nPadre1: ", "individuo", padre1Index, " ", padre1)
        # print("Padre2: ", "individuo", padre2Index, " ", padre2, "\n")

        # print("\nEtapa cruza padres\n")
        hijo1, hijo2 = cruzaUniforme(padre1, padre2) 

        # print("\nNuevos idividuos\n")
        # print("\nHijo1: ", hijo1)
        # print("\nHijo2:", hijo2, "\n")

        newPoblacion.append(hijo1)
        newPoblacion.append(hijo2)

print("Ultima generacion:", cromosomas)
poblacionFinal = decodificarCromosomas(cromosomas)
print("Valor maximo: ", max(poblacionFinal))


    