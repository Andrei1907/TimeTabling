import random
import time
import copy

import numpy as np
import math


def getMinColor(i, j, c, color, list, part, trail):
    for candidateC in range(1, c + 1):
        ok = 1
        for x in trail:
            if part[x[0]][x[1]] in list[part[j][i]]:  # nodul nou este vecin cu cel verificat
                if color[part[x[0]][x[1]]] == candidateC:
                    ok = 0
                    break
        if ok == 1:
            return candidateC
    return c + 1


def removeExtraEdges(list, part):
    nrp = len(part)
    for p in range(0, nrp):
        for i in range(0, len(part[p]) - 1):
            for j in range(i + 1, len(part[p])):
                if (part[p][j] in list[part[p][i]]):
                    list[part[p][i]].remove(part[p][j])
                    list[part[p][j]].remove(part[p][i])


def removeNodes(i, j, list, part):
    for x in range(0, len(list)):
        for y in range(0, len(list[x]) - 1):
            if j < len(part) and i < len(part[j]) and x < len(list) and y < len(list[x])-1:
                if (list[x][y] in part[j]) and (list[x][y] != part[j][i]):
                    list[x].remove(list[x][y])


def updateCD(i, j, list, part, cd, c):
    for x in range(0, len(list[part[j][i]])):
        if c not in cd[x]:
            cd[x].append(c)


# --proceduri tabuSearch--
def buildPossib(sol, maxC):
    for x in range(0, len(sol)):
        if maxC > 0:
            if sol[x] == maxC:
                if maxC == 1:
                    new = 1
                else:
                    new = random.randint(1, maxC - 1)
                sol[x] = new


def getConflicts(Q, sol, listCopy, partInit):
    for x in range(0, len(sol) - 1):
        if sol[x] > 0:
            for y in range(x, len(sol)):
                if x != y and sol[x] == sol[y] and y in listCopy[x]:
                    # print("Found conflicting color", sol[x], "between vertices", x, "in partition", partInit[x], "and", y, "in partition", partInit[y])
                    if partInit[x] not in Q:
                        Q.append(partInit[x])
                    if partInit[y] not in Q:
                        Q.append(partInit[y])


def getConflictCount(sol, listCopy):
    count = 0
    for x in range(0, len(sol) - 1):
        if sol[x] > 0:
            for y in range(x, len(sol)):
                if x != y and sol[x] == sol[y] and y in listCopy[x]:
                    count = count + 1
    return count


if __name__ == '__main__':
    # citire date despre graf: |V|, |E| si |Q| = numarul de partitii
    file1 = open("input.txt", "r")
    veq = [int(x) for x in file1.readline().split()]
    # print("|V|, |E|, respectiv |Q|:", veq)

    # stabilire partitii
    partInit = [int(file1.readline().strip()) for i in range(0, veq[0])]
    # print("Tablou partitii:", partInit)

    # stabilire muchii - matrice de adiacenta/lista de adiacenta
    matrix = np.zeros((veq[0], veq[0]), dtype=int)
    list = [[] for _ in range(veq[0])]
    for i in range(0, veq[1]):
        edge = file1.readline().split()
        matrix[int(edge[0])][int(edge[1])] = 1
        matrix[int(edge[1])][int(edge[0])] = 1
        list[int(edge[0])].append(int(edge[1]))
        list[int(edge[1])].append(int(edge[0]))

    # remodelare tablou al partitiilor
    nrp = max(partInit)
    part = [[] for _ in range(nrp + 1)]
    for index, x in enumerate(partInit):
        part[x].append(index)
    ###print("Tablou partitii remodelat:\n", part)

    partCopy = copy.deepcopy(part)
    listCopy = copy.deepcopy(list)

    start = time.time()
    # --algoritmul onestep--
    color = [0 for _ in range(veq[0])]

    # 1. Remove from G all edges (i, j) in E that link nodes in the same cluster
    removeExtraEdges(list, part)
    ###print("Lista de adiacenta modificata:\n", list)

    partialSol = []
    uncolored = [x for x in range(0, len(part))]
    cd = [[] for x in range(0, veq[0])]
    c = 1

    while len(partialSol) < veq[2]:
        X = []

        for k in uncolored:
            elem = 0
            cluster = k
            minimum = veq[0]
            for i in range(0, len(part[k])):
                if len(cd[part[k][i]]) < minimum:
                    minimum = len(cd[part[k][i]])
                    elem = i
            X.append((cluster, elem))

        maximum = len(cd[part[X[0][0]][X[0][1]]])
        x = X[0]
        for i in range(0, len(X)):
            if len(cd[part[X[i][0]][X[i][1]]]) > maximum:
                maximum = len(cd[part[X[i][0]][X[i][1]]])
                x = X[i]

        partialSol.append(x)
        uncolored.remove(x[0])
        # 10. Assign minimum colour to x
        color[part[x[0]][x[1]]] = getMinColor(x[1], x[0], c, color, list, part, partialSol)
        if (color[part[x[0]][x[1]]]) == c + 1:
            c = c + 1
        # 11. Remove from G all nodes in the same cluster as x
        removeNodes(x[1], x[0], list, part)
        # update cd for neighbour nodes of current node
        updateCD(x[1], x[0], list, part, cd, c)

    end = time.time()
    # print("\nSolutia:", color)
    # print("maxC oneStep =", max(color))
    # print("Timp total OneStep:", end - start)

    # -- procedura TabuSearch--
    start = time.time()

    tabu = []
    iter = 0
    update = True
    maxIter = veq[2] * (max(color) - 1) * 5
    # maxIter = 300
    sol = color.copy()
    maxC = max(sol)

    while iter < maxIter:
        if update:
            maxC = max(sol)
            # print("\n\n--TabuSearch--\nmaxC =", maxC)
            solPrim = sol.copy()
            buildPossib(solPrim, maxC)

            tabu = []
            iter = 0
            update = False

        Q = []
        # print(solPrim)
        getConflicts(Q, solPrim, listCopy, partInit)
        # print("Q =", Q)
        kTemp = 0
        iTemp = 0
        lTemp = 0

        while len(Q):
            kPos = random.randint(0, len(Q) - 1)
            k = Q[kPos]
            Q.remove(k)
            red = False
            maxConfl = math.comb(veq[2], 2)

            for i in range(0, len(partCopy[k])):
                for l in range(1, maxC - 1):
                    if (k, i, l) not in tabu:
                        solSec = solPrim.copy()
                        for x in range(0, len(partCopy[k])):
                            solSec[partCopy[k][x]] = 0
                        solSec[partCopy[k][i]] = l
                        # print("solSec cu i =", i, " colorat in l =", l, "din k =", k)

                        currConflCount = getConflictCount(solSec, listCopy)
                        if currConflCount < maxConfl:
                            maxConfl = currConflCount
                            solTemp = solSec
                            kTemp = k
                            iTemp = i
                            lTemp = l

                        if currConflCount < getConflictCount(solPrim, listCopy):
                            solPrim = solSec.copy()
                            red = True
                            iter = iter + 1
                            getConflicts(Q, solPrim, listCopy, partInit)
                            # print(Q)
                            break

        if getConflictCount(solPrim, listCopy) == 0:
            # print("solutie noua cu maxC =", max(solPrim))
            sol = solPrim.copy()
            maxC = maxC - 1
            update = True
        else:
            if kTemp and iTemp and lTemp:
                tabu.append((kTemp, iTemp, lTemp))
                solPrim = solTemp.copy()
            iter = iter + 1

    # print(sol)
    # print("maxC final =", max(sol))
    # print(getConflictCount(sol, listCopy), "conflicte")

    end = time.time()
    # print("Timp total TabuSearch:", end - start)

    f = open('output.txt', "w")
    for i in sol:
        f.write(str(i) + " ")
    f.close()
