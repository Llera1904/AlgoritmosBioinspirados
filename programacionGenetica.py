import operator
import math
import random

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

# Define new functions
# Para evitar el error si se divide entre cero
def protectedDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 1

pset = gp.PrimitiveSet("MAIN", 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(protectedDiv, 2)
# pset.addPrimitive(operator.neg, 1)
# pset.addPrimitive(math.cos, 1)
# pset.addPrimitive(math.sin, 1)
pset.addEphemeralConstant("rand101", lambda: random.randint(-1,1)) # Es una terminal constante puede adquirir los valores -1, 0, 1

pset.renameArguments(ARG0='x', ARG1 = 'y') # no. de entradas 

# Es una funcion de minimizacion , por eso el -1 
creator.create("FitnessMin", base.Fitness, weights=(-1.0, )) # Objeto actitud
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin) # Objeto genotipo

# Caja de herramientas, para agregar parametros 
toolbox = base.Toolbox() 
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2) # Crea individuo
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual) # Crea poblacion 
toolbox.register("compile", gp.compile, pset=pset)

# Funcion de evaluacion, recibe un individuo y devuelve la actitud correspondiente
def evalSymbReg(individual, pointsX, pointsY):
    # Transform the tree expression in a callable function
    func = toolbox.compile(expr=individual)
    # Evaluate the mean squared error between the expression
    # and the real function : x**2 + xy - y**2 
    sqerrors = (((func(x,y)) - (x**2 + x*y - y**2))**2 for x, y in zip(pointsX , pointsY))

    return math.fsum(sqerrors) / len(list(zip(pointsX, pointsY))), # Error cuadratico medio MSE

toolbox.register("evaluate", evalSymbReg, pointsX=[x/10 for x in range(-10,10)], pointsY=[y/10 for y in range(-10,10)])
toolbox.register("select", tools.selTournament, tournsize=3) # Metodo de seleccion por torneo tamaño 3
toolbox.register("mate", gp.cxOnePoint) # cruza metodo de pareja 
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2) 
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset) # Mutacion de probabilidad uniforme 

# Limita la altura de los individuos generados, por convencion es 17 
toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))

def main():
    random.seed(318)

    # Crea una poblacion 
    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(1) 

    # Calcula media, desviacion estandar, minimo y maximo de la aptitud fisica y el tamaño de los individuos 
    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    mstats.register("avg", numpy.mean)
    mstats.register("std", numpy.std)
    mstats.register("min", numpy.min)
    mstats.register("max", numpy.max)

    # Llama al algoritmo eaSimple
    pop, log = algorithms.eaSimple(pop, toolbox, 0.5, 0.1, 40, stats=mstats, halloffame=hof, verbose=True)
    # print log

    print("hof: ", *hof)

    return pop, log, hof

if __name__ == "__main__":
    main()

