import random
import time

import numpy as np


def computeCoef(i, j, pheromone, part):
    pherLevel = pheromone[part[j][i]]
    weight = len(list[part[j][i]])
    if weight == 0:
        return pherLevel*100000
    else:
        return pherLevel*(1/weight)


def getMinColor(i, j, c, color, list, part, trail):
    for candidateC in range(1, c+1):
        ok = 1
        for x in trail:
            if part[x[0]][x[1]] in list[part[j][i]]: # nodul nou este vecin cu cel verificat
                if color[part[x[0]][x[1]]] == candidateC:
                    ok = 0
                    break
        if ok == 1:
            return candidateC
    return c+1


def updatePheromoneTrails(sol, c, pheromone, pmin, pmax, evap):
    for i in range(0, len(pheromone)):
        pheromone[i] = pheromone[i] - evap
    for i in range(0, len(sol)):
        if sol[i] > 0:
            pheromone[i] = pheromone[i] + (1 - evap)/c
    for i in range(0, len(pheromone)):
        if (pheromone[i] < pmin):
            pheromone[i] = pmin
        if (pheromone[i] > pmax):
            pheromone[i] = pmax


def LocalSearchProcedure(color):
    cmax = max(color)
    cmaxPos = []
    for i in range(0, len(color)):
        if color[i] == cmax:
            cmaxPos.append(i)

    for i in range(0, len(cmaxPos)):
        # identificare cluster de care apartine
        cluster = 0
        for j in range(0, len(part)):
            if cmaxPos[i] in part[j]:
                cluster = j
                break

        exista = 0
        replacer = cmaxPos[i]
        nColor = color[replacer]

        for j in range(0, len(part[cluster])):
            if part[cluster][j] != cmaxPos[i]: # incercare pentru toate celelalte noduri din cluster
                # incercare culori mai mici decat cmax
                for c in range(cmax-1, 0, -1):
                    ok = 1
                    for v in range(0, len(list[part[cluster][j]])):
                        if color[list[part[cluster][j]][v]] == c:
                            ok = 0
                            break
                    if ok == 1:
                        replacer = part[cluster][j]
                        nColor = c
                        exista = 1
                        break
            if exista == 1:
                #print("color[", cmaxPos[i], "] = 0")
                #print("color[", replacer, "] =", nColor)
                color[cmaxPos[i]] = 0
                color[replacer] = nColor
                break
    return color


if __name__ == '__main__':
    #citire date despre graf: |V|, |E| si |Q| = numarul de partitii
    file1 = open("input.txt","r")
    veq = [int(x) for x in file1.readline().split()]
    # print("|V|, |E|, respectiv |Q|:", veq)

    #stabilire partitii
    partInit = [int(file1.readline().strip()) for i in range(0, veq[0])]
    # print("Tablou partitii:", partInit)

    #stabilire muchii - matrice de adiacenta/lista de adiacenta
    matrix = np.zeros((veq[0], veq[0]), dtype=int)
    list = [[] for _ in range(veq[0])]
    for i in range(0, veq[1]):
        edge = file1.readline().split()
        matrix[int(edge[0])][int(edge[1])] = 1
        matrix[int(edge[1])][int(edge[0])] = 1
        list[int(edge[0])].append(int(edge[1]))
        list[int(edge[1])].append(int(edge[0]))
    # print("Matrice de adiacenta:\n", matrix)
    # print("Lista de adiacenta:\n", list)



    #remodelare tablou al partitiilor
    nrp = max(partInit)
    part = [[] for _ in range(nrp+1)]
    for index, x in enumerate(partInit):
        part[x].append(index)
    # print("Tablou partitii remodelat:\n", part)

    # --algoritmul ACO--

    start = time.time()

    #valori τmax si τmin
    evap = 0.5
    pmax = 1/(1 - evap)
    pmin = 0.087 * pmax
    # print("pmax, pmin =", pmax, ",", pmin)
    pheromone = [(pmin+pmax)/2 for _ in range(veq[0])]

    nrf = 5
    # print("Numar furnici =", nrf)

    it = 0
    itMax = 10
    total = 0
    color = [0 for _ in range(veq[0])]
    optimal_val = veq[0]
    optimal_sol = []

    while it < itMax:
        #print("iteration", it)
        #update pheromone trails - based on the best solution of the current iteration
        bestCount = len(partInit)
        bestColor = [0 for _ in range(veq[0])]

        for f in range(0, nrf):
            startf = time.time_ns()

            cCluster = random.randint(0, len(part)-1)
            cNode = random.randint(0, len(part[cCluster])-1)

            color = [0 for _ in range(veq[0])]
            c = 1
            color[part[cCluster][cNode]] = c

            trail = []
            trail.append((cCluster, cNode))

            uncolored = [x for x in range(0, len(part))]
            uncolored.pop(cCluster) #clusterul cCluster tocmai a fost colorat
            uncoloredNumber = len(uncolored)

            while uncoloredNumber > 0:
                highestProb = 0
                nCluster = 0
                nNode = 0

                sum = 0
                for t in uncolored:
                    for z in range(0, len(part[t])):  # all nodes in the unused "t" cluster
                        sum = sum + computeCoef(z, t, pheromone, part)

                for j in uncolored: #for all clusters
                    for i in range(0, len(part[j])): #for all nodes in clusters
                        if (j in uncolored) and ((j, i) != (cCluster, cNode)):
                            prob = computeCoef(i, j, pheromone, part)
                            prob = prob / sum

                            if prob > highestProb:
                                highestProb = prob
                                nCluster = j
                                nNode = i

                # colorare nod nou
                color[part[nCluster][nNode]] = getMinColor(nNode, nCluster, c, color, list, part, trail)
                if(color[part[nCluster][nNode]]) == c + 1:
                    c = c + 1

                uncolored.remove(nCluster) #clusterul nCluster tocmai a fost colorat
                uncoloredNumber = len(uncolored)
                cCluster = nCluster
                cNode = nNode
                trail.append((cCluster, cNode))

            #print("furnica", f,"-> color = ", color)

            #cea mai buna (mica) solutie?
            if c < bestCount:
                bestCount = c
                bestColor = color

            endf = time.time_ns()
            #print("Timp furnica", f, ":", endf-startf)

        # local search procedure
        #print("Best solution is", bestColor)
        bestColor = LocalSearchProcedure(bestColor)

        # update pheromone trails
        #print("Best solution after LocalSearchProcedure is", bestColor)
        updatePheromoneTrails(bestColor, max(pheromone), pheromone, pmin, pmax, evap)
        #print("Pheromone trails:", pheromone, "\n")

        value = max(bestColor)
        if value < optimal_val:
            optimal_val = value
            optimal_sol = bestColor
        # print(bestColor)
        total = total + value

        # increase iteration count
        it = it + 1

    end = time.time()
    # print("\nTimp total ACO:", end-start)
    # print("AVG solution:", total/it)
    #
    # print("Best solution:", optimal_val)
    # print(optimal_sol)

    f = open('output.txt', "w")
    for i in optimal_sol:
        f.write(str(i) + " ")
    f.close()
