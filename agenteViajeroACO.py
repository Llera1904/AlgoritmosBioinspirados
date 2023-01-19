import random
import pandas as pd
import numpy as np
import graphviz as gv

class ACO:
    def __init__(self, numberNodes, a, b, p, maxIterations):
        self.numberNodes = numberNodes 
        self.a = a # Alpha
        self.b = b # Beta
        self.p = p # Factor de perdida
        self.maxIterations = maxIterations

    def pheromonesAndDistances(self):
        np.random.seed(0)
        # distanceMatrix = np.random.uniform(10, 200, (self.numberNodes, self.numberNodes)) # Distancias random
        distanceMatrix = np.random.randint(10, 200, (self.numberNodes, self.numberNodes)) # Distancias random (enteras)
        pheromones = np.random.uniform(0, 1, (self.numberNodes, self.numberNodes)) # Feromonas random
        for i in range(self.numberNodes):
            distanceMatrix[i, :i+1] = distanceMatrix[:i+1, i] # Distancias al contrario iguales (d1 a d2 = d2 a d1)
            pheromones[i, :i+1] = pheromones[:i+1, i]
            distanceMatrix[i, i] = 1 # Distancia con el mismo nodo (evita la division entre cero)
            pheromones[i, i] = 0
        df = pd.DataFrame(distanceMatrix)
        df2 = pd.DataFrame(pheromones)
        print("\nMatriz de distancias:\n", df)
        print("\nMatriz de feromonas:\n", df2, "\n")

        return distanceMatrix , pheromones

    def nodeSelection(self, probabilities): # Selecciona a que nodo moverse por el metodo de la ruleta 
        valueRandom = random.uniform(0, 1) 
        probabilitiesAcumulated = np.cumsum(probabilities, axis=0) # Probabilidad acumulada 
        probabilitiesAcumulated[np.array(self.forbiddenList)] = np.inf 
        differences = np.abs(probabilitiesAcumulated - valueRandom)
        nodeSelect = differences.tolist().index(min(differences)) # Obtiene el siguiente nodo 

        # print("N random:", valueRandom)
        # print("P acumulada:", probabilitiesAcumulated)
        # print("Nodo seleccionado:", nodeSelect)

        return nodeSelect

    def traverseGraph(self, currentNode):
        if len(self.forbiddenList) == self.numberNodes - 1:
            self.forbiddenList.append(currentNode)
            return 
        self.forbiddenList.append(currentNode) # Agregamos el nodo actual a los nodos visitados (prohibidos)

        denominator = (self.pheromones[currentNode, :] ** self.a) * ((1 / self.distanceMatrix[currentNode, :]) ** self.b)
        denominator[np.array(self.forbiddenList)] = 0 # Pone en cero los valores de los nodos que ya se visitaron 
        probabilities = denominator / np.sum(denominator)
        # print("P:", probabilities)

        nextNode = self.nodeSelection(probabilities)
        self.distanceTraveled += self.distanceMatrix[currentNode, nextNode]
        self.traverseGraph(nextNode)

        self.antPheromones[currentNode, nextNode] += 1 / self.distanceTraveled # Guarda la feronomona dejada por la hormiga
        self.antPheromones[nextNode, currentNode] = self.antPheromones[currentNode, nextNode]

        return 

    def getBestPath(self):
        return self.bestPath

    def updatePheromones(self): # Actualiza las feromonas una vez completado el recorrido 
        self.pheromones *= (1 - self.p)
        self.pheromones += self.antPheromones
    
    def drawGraph(self):
        # Crea la ventana
        g = gv.Digraph(format='svg')
        g.graph_attr['rankdir'] = 'LR' # Pinta el grafico de izquierda a derecha 

        # Crea la lista de las ciudades
        cities = []
        for i in range(self.numberNodes):
            cities.append("ciudad" + str(i))

        # Crea los nodos de las ciudades
        for city in range(self.numberNodes):
            g.node(cities[city])

        # Crea una lista de tuplas del mejor camino
        pathEdges = []
        for node in range(len(bestPath[0]) - 1):
            pathEdges.append([bestPath[0][node], bestPath[0][node + 1]])
        # print(pathEdges)

        # Hace las conexiones entre nodos
        for i in range(self.numberNodes):
            for j in range(self.numberNodes):
                if i != j:
                    if [i, j] in pathEdges:
                        g.edge(cities[i], cities[j], label=str(self.distanceMatrix[i][j]), color="red", penwidth="3.0")
                    else:
                        g.edge(cities[i], cities[j], label=str(self.distanceMatrix[i][j]))
                        
        return g   

    def fit(self):
        self.distanceMatrix, self.pheromones = self.pheromonesAndDistances() # Crea aleatoriamente las distancias y las feromonas
        self.bestPath = [[], np.inf] # Guardara el mejor camino y la mejor distancia 
        with open("Iterations.txt", "w") as file:
            for i in range(self.maxIterations):
                file.write("Iteracion: "+ str(i) + "\n")
                self.paths = []
                self.distancesTraveled = []
                self.antPheromones = np.zeros((self.numberNodes, self.numberNodes), dtype=np.float32)
                for _ in range(self.numberNodes):
                    self.forbiddenList = [] # Nodos visitados 
                    self.distanceTraveled = 0
                    self.traverseGraph(0) # Recorre el grafo 
                    self.paths.append(self.forbiddenList) 
                    self.distancesTraveled.append(self.distanceTraveled)  
                    file.write("Camino: " + str(self.forbiddenList) + " Distancia: " + str(self.distanceTraveled) + "\n")
                bestIndex = self.distancesTraveled.index(min(self.distancesTraveled)) # Indice de la ruta mas corta 
                file.write("Mejor camino: " + str(self.paths[bestIndex]) + "  " + str(self.distancesTraveled[bestIndex]) + "\n\n")

                if self.distancesTraveled[bestIndex] < self.bestPath[1]: # Actualiza el mejor camino 
                    self.bestPath[0] = self.paths[bestIndex]
                    self.bestPath[1] = self.distancesTraveled[bestIndex]

                self.updatePheromones() # Actualiza feromonas 
 
antAlgorithm = ACO(numberNodes=10, a=1.5, b=1, p=0.1, maxIterations=2000)
antAlgorithm.fit()
bestPath = antAlgorithm.getBestPath()
print("Mejor camino:\n", bestPath)
g = antAlgorithm.drawGraph()
g.view()