import random
import math
import pandas as pd
import numpy as np

def population(particleNumber, sizeVector): # Crea una poblacion de particulas y velocidades iniciales
    particles = []
    speeds = []
    for i in range(particleNumber):
        particle = np.zeros(2, dtype=np.float16)
        speed = np.zeros(2, dtype=np.float16)
        for j in range(sizeVector):
            randomNumber = random.uniform(-5, 5) 
            particle[j] = randomNumber
            speed[j] = 0 # Inicializa las velocidades en 0
        particles.append(particle)
        speeds.append(speed)
    
    return speeds, particles

def objectiveFunction(particles): # Funcion onjetivo 
    evaluatedValues = []
    for particle in particles:
        result = particle[0]**2 + particle[1]**2 # x**2 + y**2
        evaluatedValues.append(result)

    return evaluatedValues

def bestParticle(evaluatedValues, particles):
    bestParticleIndex = evaluatedValues.index(min(evaluatedValues)) # Indice de la mejor particula
    value = evaluatedValues[bestParticleIndex]
    # print("\nIndice de la mejor particula: ", bestParticleIndex)

    return particles[bestParticleIndex], value

def particleSpeed(Gbest, Pbest, particles, speeds, sizeVector, a, b1, b2): # Calcula la velocidad de las particulas 
    newSpeeds = []
    for bestParticle, particle, speed in zip(Pbest, particles, speeds):
        newSpeed = np.zeros(2, dtype=np.float16)
        for i in range(sizeVector):
            r1 = random.uniform(0, 1) # Calcula los factores de aleatoridad entre [0, 1]
            r2 = random.uniform(0, 1)
            # print("Factor random: ", r1, ", ", r2)
            newSpeed[i] = (a * speed[i]) + ((b1 * r1) * (bestParticle[i] - particle[i])) + ((b2 * r2) * (Gbest[i] - particle[i])) 
        newSpeeds.append(newSpeed)
    # print("\nNuevas velocidades:\n", *newSpeeds)

    return newSpeeds

def updatePosition(particles, speeds, sizeVector): # Actualiza las posiciones de las particulas 
    newParticles = []
    for particle, speed in zip(particles, speeds):
        newParticle = np.zeros(2, dtype=np.float16)
        for i in range(sizeVector):
            newPos = particle[i] + speed[i]
            if newPos > -5 and newPos < 5: # Restringe el valor de la particula al intervalo [-5, 5]
                newParticle[i] = newPos
            elif newPos < -5:
                newParticle[i] = -5
            elif newPos > 5:
                newParticle[i] = 5
        newParticles.append(newParticle)
    # print("\nNuevas particulas:\n", *newParticles)

    return newParticles

def updatePbest(particles, Pbest, evaluatedValues, evaluatedValuesPbest):
    newPbest = []
    for particle, bestParticle, evaluatedValue, evaluatedValuePbest in zip(particles, Pbest, evaluatedValues, evaluatedValuesPbest):
        if evaluatedValue < evaluatedValuePbest:
            newPbest.append(particle)
        elif evaluatedValuePbest < evaluatedValue:
            newPbest.append(bestParticle)
        elif evaluatedValuePbest == evaluatedValue:
            newPbest.append(bestParticle)
    # print("\nPbest:\n", *newPbest)

    return newPbest
           
# Parametros
particleNumber = 20 # Numeo de particulas
sizeVector = 2 # Tamaño del vector de las particulas 
a = 0.8 # Inercia
b1 = 0.7 # Factor de aprendizaje (Propia)
b2 = 1 # Factor de aprendizaje (Social)
iterations = 50 # Numero de iteraciones 

# Inicializacion del algoritmo 
speeds, particles = population(particleNumber, sizeVector) # Poblacion inicial de particulas y velocidades 
evaluatedValues = objectiveFunction(particles) # Evalua las particulas en la funcion objetivo
Pbest = particles # Al inicio las mejores particulas son las mismas que las iniciales
evaluatedValuesPbest = evaluatedValues
Gbest, valueGbest = bestParticle(evaluatedValues, Pbest) # Busca cual es la mejor particula 

data = list(zip(speeds, particles, evaluatedValues, Pbest, evaluatedValuesPbest))
df = pd.DataFrame(data, columns=["Speeds", "Particles", "EvaluatedValues", "Pbest", "EvaluatedValuesPbest"])
print(df)
print("Gbest: ", Gbest)
print("Valor: ", valueGbest, "\n")

# Inicia parte iterativa
for i in range(iterations):
    speeds = particleSpeed(Gbest, Pbest, particles, speeds, sizeVector, a, b1, b2) # Calcula la velocidad de las particulas
    particles = updatePosition(particles, speeds, sizeVector) # Actualiza la posicion de las particulas 
    evaluatedValues = objectiveFunction(particles) # Evalua las particulas en la funcion objetivo 
    Pbest = updatePbest(particles, Pbest, evaluatedValues, evaluatedValuesPbest) 
    evaluatedValuesPbest = objectiveFunction(Pbest)
    Gbest, valueGbest = bestParticle(evaluatedValues, Pbest)

    data = list(zip(speeds, particles, evaluatedValues, Pbest, evaluatedValuesPbest))
    df = pd.DataFrame(data, columns=["Speeds", "Particles", "EvaluatedValues", "Pbest", "EvaluatedValuesPbest"])
    print(df)
    print("Gbest: ", Gbest)
    print("Valor: ", valueGbest, "\n")