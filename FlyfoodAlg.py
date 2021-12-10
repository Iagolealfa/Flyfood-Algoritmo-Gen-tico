
import random
import matplotlib.pyplot as plt
import time

def dist_dos_pontos(ponto_a, ponto_b):
  return (abs(ponto_a[0]-ponto_b[0]) + abs(ponto_a[1]-ponto_b[1]))

def dist_total(pontos, caminho):
  distancia_total=0
  ponto_anterior=pontos["R"]

  for ponto in caminho:
    distancia_total+=dist_dos_pontos(pontos[ponto],ponto_anterior)
    ponto_anterior=pontos[ponto]
  
  distancia_total+=dist_dos_pontos(ponto_anterior,pontos["R"])
  return distancia_total
def gerar_populacao_inicial(populacao,tamanho_populacao):
    populacao_inicial=[None]*tamanho_populacao
    for x in range(tamanho_populacao):
        estado=populacao[:]
        random.shuffle(estado)
        populacao_inicial[x]=estado
    return populacao_inicial

def calc_aptidao(local_mapa,individuos):
    resultados=[None]*len(individuos)
    for x,individuo in enumerate(individuos):
        aptidao=dist_total(local_mapa,individuo)
        resultados[x]=(individuo,aptidao)
    return resultados

def rank_aptidao(resultados):
  return sorted(resultados,key=lambda resultado:resultado[1])

def selecao_populacao(populacao, participantes_do_torneio, tamanho_elite):
    individuos_mais_aptos=[None]*len(populacao)
    for x in range(0,tamanho_elite):
        individuos_mais_aptos[x]=populacao[x][0]

    for x in range(tamanho_elite,len(populacao)):
        torneio=random.sample(populacao,participantes_do_torneio)
        campeao_do_torneio=min(torneio,key=lambda lutador: lutador[1])
        individuos_mais_aptos[x]=campeao_do_torneio[0]
    return individuos_mais_aptos

def PMX(pai_1, pai_2):
  filhos=[None] * 2
  pai=pai_1
  copia_pai=pai_2[:]
  ponto_de_cruzamento=random.randint(1, len(pai) - 1)

  for filho in range(len(filhos)):
      for ponto in range(ponto_de_cruzamento):
        if(pai[ponto]!=copia_pai[ponto]):
          temp=copia_pai[ponto]
          copia_pai[ponto]=pai[ponto]
          for ponto_a_trocar in range(ponto+1,len(copia_pai)):
            if(copia_pai[ponto]==copia_pai[ponto_a_trocar]):
              copia_pai[ponto_a_trocar]=temp
              break
      filhos[filho]=copia_pai
      pai=pai_2
      copia_pai=pai_1[:]
  return filhos

def mutacao(individuo, probabilidade):
  for x in range(len(individuo)):
    if(random.random()<=probabilidade):
      index_aleatorio=random.randint(0, len(individuo) - 1)
      individuo[x],individuo[index_aleatorio]=individuo[index_aleatorio],individuo[x]  

def main():
    l ,c=list(map(int,input().split()))
    inicio = time.time()
    matrix=[]
    for x in range(l):
        linha=input().split()
        matrix.append(linha)
    todos_pontos=dict()
    pontos_entrega=[]
    for x in range(l):
        for y in range(c):
            if matrix[x][y]!='0':
                todos_pontos[matrix[x][y]]=[x, y]
            if matrix[x][y]!='0' and matrix[x][y]!='R':
                pontos_entrega.append(matrix[x][y])

    tam_populacao=100
    geracoes=100
    part_torneio=2
    taxa_de_mutacao=0.01
    tam_elite=20           
    desenvolvimento=[]
    geracao=gerar_populacao_inicial(pontos_entrega,tam_populacao)
    resultados=calc_aptidao(todos_pontos,geracao)            
    result_ordenados_por_aptidao = rank_aptidao(resultados)
    melhor_individuo = result_ordenados_por_aptidao[0]
    desenvolvimento.append(result_ordenados_por_aptidao[0][1])
    print("Distancia inicial:",  result_ordenados_por_aptidao[0][1])

    for y in range(geracoes):

        filhos=list()
        individuos_para_cruzamento=selecao_populacao(result_ordenados_por_aptidao, part_torneio, tam_elite)
        for index in range(0, len(individuos_para_cruzamento), 2):

          mod=index % (len(individuos_para_cruzamento) - 1)
          pai_1=individuos_para_cruzamento[mod]
          pai_2=individuos_para_cruzamento[mod + 1]
          for filho in PMX(pai_1, pai_2):
            mutacao(filho, taxa_de_mutacao)
            filhos.append(filho)

        geracao=filhos
        resultados=calc_aptidao(todos_pontos, geracao)
        result_ordenados_por_aptidao=rank_aptidao(resultados)

        desenvolvimento.append(result_ordenados_por_aptidao[0][1])
        if(result_ordenados_por_aptidao[0][1]<melhor_individuo[1]):
            melhor_individuo=result_ordenados_por_aptidao[0]
    fim = time.time()    
    print("tempo", fim - inicio)  

    print("Menor distância encontrada:", melhor_individuo[1])
    print("Menor caminho: R ->", (" -> ").join(melhor_individuo[0]), "-> R")
    plt.figure(figsize=(8, 6), dpi=80)
    plt.plot(desenvolvimento)
    plt.ylabel('Distância')
    plt.xlabel('Geração')
    plt.show()
    return melhor_individuo




if __name__ == '__main__':
    main()                 