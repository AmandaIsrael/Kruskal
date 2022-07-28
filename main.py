import time
import pandas as pd
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
    tempo_quadratico = time.time() - t0           
    return tempo_quadratico, num_comp_quadratico, agm

def union_find(arestas_hash, tamanho_conjunto):
    agm = []
    keys = [int(key) for key in arestas_hash.keys()]
    keys.sort()
    for key in keys:
        l = arestas_hash[str(key)]
        for ele in l:
            print(ele)
    return tempo_union_find, num_comp_union_find

if __name__=="__main__":
    tamanhos_conjuntos = [10, 25, 50, 75, 100, 150, 200, 250, 300, 400, 500, 650, 800, 1000, 1500]
    
    arestas_hash = leitura_matriz(10)
    tempo_quadratico, num_comp_quadratico, agm = quadratico(arestas_hash, 10)
    print(tempo_quadratico, num_comp_quadratico, agm)
"""
    for tamanho_conjunto in tamanhos_conjuntos:
        arestas_hash = leitura_matriz(tamanho_conjunto)
        tempo_quadratico, num_comp_quadratico = quadratico(arestas_hash, tamanho_conjunto)
        tempo_union_find, num_comp_union_find = union_find(arestas_hash, tamanho_conjunto)
        results = pd.DataFrame({
                'Tempo quadrático': [tempo_quadratico],
                'Tempo Union Find':[tempo_union_find],
                'Número de comparações quadrático':[num_comp_quadratico],
                'Número de comparações Union Find': [num_comp_union_find],
                'Tamanho':[tamanho_conjunto]
            })
        
        if exists("Reultados.csv"):
            file_df = pd.read_csv("Reultados.csv")
            file_df = pd.concat([file_df,results], ignore_index=True)
            file_df.to_csv("Reultados.csv",index=False)
        else:
            results.to_csv("Reultados.csv",index=False)
            
        t1 = time.time()
        print(f"Tempo decorrido: {round(t1-t0,6)} seg")
        print("-"*10)
        """
