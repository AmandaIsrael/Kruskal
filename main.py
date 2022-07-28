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
                arestas_hash[ele].append([i,j])

    return arestas_hash

def quadratico(arestas_hash, tamanho_conjunto):
    agm = []
    keys = [int(key) for key in arestas_hash.keys()]
    keys.sort()
    for key in keys:
    l = arestas_hash[str(key)]
    for ele in l:
        print(ele)
    return tempo_quadratico, num_comp_quadratico

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
    
    print(leitura_matriz(10))
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
