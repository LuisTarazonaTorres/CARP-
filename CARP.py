# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 15:11:34 2022

@author: Luis Tarazona
"""

import igraph as ig
import matplotlib.pyplot as plt
from copy import copy
import pandas as pd
from time import time
import matplotlib.pyplot as plt



start = time()

def cargar_instancia(file_name):
#nodos y costos
    Arcos = []
    Nodos = []
    costos = {}
    
    file = open(file_name)
    file = file.readlines()
    for fila in file[2:]:
        if fila[1] == '-':
            primer_nodo = int(fila[0])
            if fila[3] == '-':
                segundo_nodo = int(fila[2])
                arco = (primer_nodo, segundo_nodo)
                Arcos.append(arco)
                if fila[5] == '-':                
                    costo = int(fila[4])
                    costos[arco] = costo
                else:
                    costo = int(fila[4:6])
                    costos[arco] = costo
            else: 
                segundo_nodo = int(fila[2:4])
                arco = (primer_nodo, segundo_nodo)
                Arcos.append(arco)
                if fila[7] == '-':
                    costo = int(fila[5:7])
                    costos[arco] = costo
                else: 
                    costo = int(fila[5])
                    costos[arco] = costo
        else:
            primer_nodo = int(fila[0:2])
            segundo_nodo = int(fila[3:5])
            arco = (primer_nodo, segundo_nodo)
            Arcos.append(arco) 
            if fila[7] == '-':
                costo = int(fila[6])
                costos[arco] = costo
            else:
                costo = int(fila[6:8])
                costos[arco] = costo
        
        if primer_nodo not in Nodos:
            Nodos.append(primer_nodo)
        if segundo_nodo not in Nodos:
            Nodos.append(segundo_nodo)
    
    #capacidad (W) y n° de vehículos (K)
    W = int(file[0])
    
    K = int(file[1])
    
    num_nodos = int(len(Nodos))

    
    num_arcos = int(len(costos))

    
    
    
    return Arcos, Nodos, costos, W, K, num_nodos, num_arcos
    
#%%
##La ruta más corta con Dijkstra


def dijkstra(num_nodos, Arcos, costos):
    results = {}
    distance= {}
    costos = list(costos.values())

    g = ig.Graph(num_nodos, Arcos, edge_attrs = {"weight":costos})
# g.get_shortest_paths() returns a list of vertex ID paths
    for i in range(num_nodos):
        for j in range(num_nodos):
            results[i,j] = g.get_shortest_paths(i, to=j, output="vpath")[0]      
            distancee = 0
            results2 = g.get_shortest_paths(i, to=j, weights=costos, output="epath",)
            for e in results2[0]:
                distancee += g.es[e]["weight"]
            distance[i,j] = int(distancee)
            
    return results, distance
    
#%%
## Completar evaluación de todas las instancias
file_name = 'Instancia7.txt'
Arcos, Nodos, costos, W, K, num_nodos, num_arcos = cargar_instancia(file_name)


results, distance = dijkstra(num_nodos, Arcos, costos)


D = {i:1 for i in Arcos}


arcos_pendiente = copy(Arcos)
nodos_pendiente = copy(Nodos)
num_rutas = 1
rutas = {}
costox = {}
while len(arcos_pendiente) > 0:
    
    rutas[num_rutas] = [0]
    nodo_inicio = 0
    ruta_lista = False
    costox[num_rutas] = 0
    barrido = []
    recogido = 0
    
    while not ruta_lista:

        ####Encontrar el nodo más cercano 
        distances = 1000000000000
        ruta_lista = True
        for candidato in nodos_pendiente:
            sihay = False
            for arco in arcos_pendiente:
                if (arco[0] == candidato or arco[1] == candidato) and recogido + D[arco] <= W:
                    print(recogido + D[arco] <= W)
                    sihay = True
                    
                
            if distance[nodo_inicio, candidato] < distances and sihay:
                distances = distance[nodo_inicio, candidato]
                costox[num_rutas] = distance[nodo_inicio, candidato]
                nodo_final = candidato
                ruta_lista = False 

        # print(recogido)       
        # print(ruta_lista)
        if not ruta_lista:

            ####Encontrar el mejor arco 
            mejor_arco =()
            mejor_costo = 100000000000000
            for arco in arcos_pendiente:
                if arco[0] == nodo_final or arco[1] == nodo_final and D[arco] + recogido <= W:
                    if costos[arco] < mejor_costo:
                        mejor_arco = arco
                        mejor_costo = costos[arco]
                       
            if nodo_final != nodo_inicio:
                rutas[num_rutas] += results[nodo_inicio, nodo_final][1:]
            

            
            if mejor_arco[0] == nodo_final:
                finalll = mejor_arco[1]
            else:
                finalll = mejor_arco[0]

            rutas[num_rutas] += [finalll]

            ### COSTOS
            costox[num_rutas] += distance[tuple(mejor_arco)]
            barrido.append(mejor_arco)
            mejor_arco = tuple(mejor_arco)
            arcos_pendiente.remove(mejor_arco)
            
            
            si_tiene = False
            for arco in arcos_pendiente:
                if arco[0] == nodo_final or arco[1] == nodo_final:
                    si_tiene = True
        
            if not si_tiene:
                nodos_pendiente.remove(nodo_final)

            si_tiene = False
            for arco in arcos_pendiente:
                if arco[0] == finalll or arco[1] == finalll:
                    si_tiene = True
            
            if not si_tiene:
                nodos_pendiente.remove(finalll)
            
            recogido += D[mejor_arco]
            nodo_inicio = finalll
        
    ##cerrar ruta y regresar al depósito
    rutas[num_rutas] += results[finalll,0][1:]
    costox[num_rutas] += distance[finalll,0]
    
    num_rutas += 1
    


print(rutas)


##costo total
b = []
for x in range(1,len(rutas)+1):
    for y in range(0,len(rutas[x])-1):
        b.append(distance[rutas[x][y],rutas[x][y+1]])

print("el costo total es igual: ", sum(b))

times = time() - start
print(times)