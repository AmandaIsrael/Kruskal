import time
import pandas as pd
import os
from os.path import exists
pd.set_option("display.precision", 6)

def abrir_arquivos(tamanho_conjunto):
    with open("Entradas/Entrada "+str(tamanho_conjunto)+".txt", "r") as arquivo:
        arquivo.readline()
        matriz = []
        for linha in arquivo:
            valores_string = linha.split(" ")[:-1]
            matriz.append(valores_string)

    return matriz

def leitura_matriz(tamanho_conjunto):

    matriz = abrir_arquivos(tamanho_conjunto)
    arestas_hash = {}

    for i in range(tamanho_conjunto):
        for j in range(i + 1, tamanho_conjunto):
            ele = matriz[i][j]
            if ele != '0':
                if not ele in arestas_hash:
                    arestas_hash[ele] = []
                arestas_hash[ele].append(tuple([i,j]))

    return arestas_hash

def quadratico(arestas_hash, tamanho_conjunto):
    agm = []
    keys = [int(key) for key in arestas_hash.keys()]
    keys.sort()
    list_vertices_visitados = []
    num_comp_quadratico = 0
    t0 = time.time()
    for key in keys:        
        l = arestas_hash[str(key)]
        for ele in l:
            first = -1
            second = -1
            for ind_conjunto in range(len(list_vertices_visitados)):
                for vert in list_vertices_visitados[ind_conjunto]:
                    num_comp_quadratico += 1
                    if vert == ele[0]: first = ind_conjunto
                    if vert == ele[1]: second = ind_conjunto
                    if first != -1 and second != -1: break
            if first == -1 and second == -1:
                agm.append(ele)
                list_vertices_visitados.append([ele[0], ele[1]])
            elif first != -1 and second == -1:
                agm.append(ele)
                list_vertices_visitados[first].append(ele[1])
            elif first == -1 and second != -1:
                agm.append(ele)
                list_vertices_visitados[second].append(ele[0])
            elif first != second:
                conjunto = list_vertices_visitados.pop(max(first, second))
                list_vertices_visitados[min(first, second)].extend(conjunto)
                agm.append(ele)
            if tamanho_conjunto == len(list_vertices_visitados[0]):
                break
        if tamanho_conjunto == len(list_vertices_visitados[0]):
            break
    
    t1 = time.time()
    tempo_quadratico = (t1*100)-(t0*100)           
    return tempo_quadratico, num_comp_quadratico, agm

def get_root(arvores, vertice, count):
    if arvores[vertice][0] == vertice:
        return vertice, count
    else:
        count += 1
        return get_root(arvores, arvores[vertice][0], count)

def union_find(arestas_hash, tamanho_conjunto):
    agm = []
    arvores = []
    num_comp_union_find = 0

    keys = [int(key) for key in arestas_hash.keys()]
    keys.sort()

    t0 = time.time()
    stop = False
    for i in range(tamanho_conjunto):
        arvores.append([i,1])

    for key in keys:
        l = arestas_hash[str(key)]
        for ele in l:
            root_first, count_first = get_root(arvores, ele[0], 1)
            root_second, count_second = get_root(arvores, ele[1], 1)
            num_comp_union_find += count_first + count_second

            if root_first != root_second:
                agm.append(ele)
                if arvores[root_first][1] >= arvores[root_second][1]:
                    arvores[root_second][0] = root_first
                    arvores[root_first][1] += arvores[root_second][1]
                    if arvores[root_first][1] == tamanho_conjunto:
                        stop = True
                else:
                    arvores[root_first][0] = root_second
                    arvores[root_second][1] += arvores[root_first][1]
                    if arvores[root_second][1] == tamanho_conjunto:
                        stop = True

                if stop:
                    break
            
        if stop:
            break
                
    t1 = time.time()

    tempo_union_find = (t1*100)-(t0*100)
    return tempo_union_find, num_comp_union_find, agm

if __name__=="__main__":
    os.nice(-19)
    tamanhos_conjuntos = [10, 25, 50, 75, 100, 150, 200, 250, 300, 400, 500, 650, 800, 1000, 1500]

    for tamanho_conjunto in tamanhos_conjuntos:
        print(f"TAMANHO {tamanho_conjunto}")
        arestas_hash = leitura_matriz(tamanho_conjunto)
        total_tempo_quadratico, total_tempo_union_find = 0,0
        for i in range(100):
            tempo_quadratico, num_comp_quadratico, agm_quadratico = quadratico(arestas_hash, tamanho_conjunto)
            tempo_union_find, num_comp_union_find, agm_union_find = union_find(arestas_hash, tamanho_conjunto)
            total_tempo_quadratico += tempo_quadratico
            total_tempo_union_find += tempo_union_find
        print(f"{total_tempo_quadratico/100} ms, {num_comp_quadratico} comparações")
        print(f"{total_tempo_union_find/100} ms, {num_comp_union_find} comparações")
        print("AGMs iguais" if agm_quadratico==agm_union_find else "AGMs diferentes")
        print("-"*20)
        results = pd.DataFrame({
                'Tamanho':[tamanho_conjunto],
                'Tempo quadrático': [total_tempo_quadratico/100],
                'Número de comparações quadrático':[num_comp_quadratico],
                'Quadratico (Tempo/Mil Comparações)': [(total_tempo_quadratico/100)*1000/num_comp_quadratico],
                'Tempo Union Find':[total_tempo_union_find/100],
                'Número de comparações Union Find': [num_comp_union_find],
                'Union Find (Tempo/Mil Comparações)': [(total_tempo_union_find/100)*1000/num_comp_union_find]
                
            })
        
        if exists("Reultados.csv"):
            file_df = pd.read_csv("Reultados.csv")
            file_df = pd.concat([file_df,results], ignore_index=True)
            file_df.to_csv("Reultados.csv",index=False)
        else:
            results.to_csv("Reultados.csv",index=False)
