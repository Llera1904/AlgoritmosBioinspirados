import random
import pandas as pd
import numpy as np

def foodFountains(workerBees, lowerLimit, upperLimit, sizeSolution):
    random.seed(0)
    foodFountain = np.zeros((workerBees, sizeSolution), np.float32) # Fuentes de comida 
    with np.nditer(foodFountain, flags=["multi_index"], op_flags=["readwrite"]) as it:
        for food in it:
            numberRandom = random.uniform(0, 1)
            food[...] = lowerLimit + numberRandom * (upperLimit - lowerLimit) # 1er formula
            # print(it.multi_index, food)
    # print(foodFountain)

    return foodFountain.copy()

def newFoodFountain(foodFountain, fitnessValues, limits, lowerLimit, upperLimit, sizeSolution, i): 
    j = random.randint(0, sizeSolution - 1)
    while 1:
        k = random.randint(0, len(foodFountain) - 1)
        if k != i:
            break
    numberRandom = random.uniform(-1, 1)
    newPosition = foodFountain[i, j] + (numberRandom * (foodFountain[i, j] - foodFountain[k, j])) # 2da formula 

    if newPosition < lowerLimit: # Restringimos los valores de la nueva posicion 
        newPosition = lowerLimit
    elif newPosition > upperLimit:
        newPosition = upperLimit

    newSolution = foodFountain[i].copy()
    newSolution[j] = newPosition # Actualiza la posicion j-esima
    fitnessNewSolution = objectiveFunction([newSolution])[0] # Fitness de la solucion (Regresa una lista)

    if fitnessNewSolution < fitnessValues[i]:  
        foodFountain[i] = newSolution.copy() # Actualiza la solucion
        fitnessValues[i] = fitnessNewSolution # Actualiza el fitness
        limits[i] = 0  
    elif fitnessNewSolution >= fitnessValues[i]:
        limits[i] += 1

def foodFountainSelection(probabilitiesAcumulated): # Selecciona una fuente de comida por el metodo de la ruleta 
    # Calculamos la diferencia entre el valor random y la 
    # probabilidad de seleccion acumulada de cada fuente de comida
    differences = []
    valueRandom = random.uniform(0, 1) 
    for fountainProbability in probabilitiesAcumulated:
        difference = abs(fountainProbability - valueRandom)
        differences.append(difference)
    fountainSelect = differences.index(min(differences)) # Obtiene la fuente de comida

    return fountainSelect

def objectiveFunction(foodFountain): # Funcion objetivo 
    evaluatedValues = []
    for food in foodFountain:
        result = food[0]**2 + food[1]**2 # x**2 + y**2
        evaluatedValues.append(result)

    return evaluatedValues.copy()
    
# Parametros   
bees = 40 # Abejas totales (Tamaño de enjambre)
workerBees = int(bees / 2) # Abejas obreras (%50)
observantBees = int(bees / 2) # Abejas observadoras (%50)
iterations = 50
limit = 10

lowerLimit = -5 # Limite inferior
upperLimit = 5 # Limite superior 
sizeSolution = 2 # Tamaño de la solucion 

# Inicializacion
foodFountain = foodFountains(workerBees, lowerLimit, upperLimit, sizeSolution) # Inicializamos las fuentes de comida 
fitnessValues = objectiveFunction(foodFountain) # Nectar de la fuente de comida (Fitness de cada solucion)
limits = np.zeros((workerBees), dtype=np.int32) # Limites incializados en cero 
data = list(zip(foodFountain, fitnessValues, limits))
df = pd.DataFrame(data, columns=["foodFountain", "fitnessValues", "limits"])
print(df, "\n")

bestSolution = [[], np.inf] # Guardara la mejor solucion 
with open("Iterations.txt", "w") as file:
    for iter in range(iterations):
        file.write("Iteracion: "+ str(iter) + "\n")

        # Fase de abejas obreras
        for i in range(workerBees):
            newFoodFountain(foodFountain, fitnessValues, limits, lowerLimit, upperLimit, sizeSolution, i)

        # Fase de abejas observadoras
        probabilities = [] 
        probabilitiesAcumulated = []
        sumProbabilities = 0
        for fit in fitnessValues: # Calcula la probabilidad de cada solucion y la probabilidad acumulada 
            # if sum(fitnessValues) != 0: # Evita la division entre cero
            #     if fit >= 0:
            #         fit = 1 / (1 + fit)
            #     else:
            #         fit = 1 + abs(fit)
            #     probability = fit / sum(fitnessValues)
            # else:
            #     probability = 0

            if fit >= 0:
                fit = 1 / (1 + fit)
            else:
                fit = 1 + abs(fit)
            probability = fit / sum(fitnessValues)
            
            sumProbabilities += probability
            probabilities.append(probability)
            probabilitiesAcumulated.append(sumProbabilities)
        # print(probabilities)
        # print(probabilitiesAcumulated)

        for i in range(observantBees):
            numberRandom = random.uniform(0, 1)
            fountainSelect = foodFountainSelection(probabilitiesAcumulated) # Selecciona una fuente de comida o abeja obrera a la cual seguir 
            if numberRandom < probabilities[fountainSelect]: # Sale la abeja observadora   
                newFoodFountain(foodFountain, fitnessValues, limits, lowerLimit, upperLimit, sizeSolution, fountainSelect) # Modifica la fuente seleccionada

        # Fase de abejas exploradoras
        for i in range(len(limits)):
            if limits[i] >= limit: # La abeja se hace exploradora (Se abandona solucion)
                newSolution = foodFountains(1, lowerLimit, upperLimit, sizeSolution)[0] # Crea una nueva solucion (Regresa una lista)
                fitnessNewSolution = objectiveFunction([newSolution])[0] # Fitness de la solucion (Regresa una lista)
                foodFountain[i] = newSolution.copy() # Actualiza la fuente de comida 
                fitnessValues[i] = fitnessNewSolution # Actualiza el fitness
                limits[i] = 0

        data = list(zip(foodFountain, fitnessValues, limits))
        df = pd.DataFrame(data, columns=["foodFountain", "fitnessValues", "limits"])
        # print(df)
        file.write(str(df) + "\n")

        bestIndex = fitnessValues.index(min(fitnessValues)) # Indice de la mejor solucion  
        # print("Mejor solucion:", foodFountain[bestIndex], fitnessValues[bestIndex], "\n")
        file.write("Mejor solucion:" + str(foodFountain[bestIndex]) + "  " + str(fitnessValues[bestIndex]) + "\n\n")
        if fitnessValues[bestIndex] < bestSolution[1]: # Actualiza la mejor solucion 
            bestSolution[0] = foodFountain[bestIndex]
            bestSolution[1] = fitnessValues[bestIndex]  
print("Mejor solucion:", bestSolution[0], bestSolution[1])                                                                                                                      