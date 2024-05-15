import bancodedadosnovo
import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt
from scipy import signal

def calcular_04395(pesosub, pesoar, temp, diametro, altura, asfato, id_ensaio):
    vetor_calculados =[]
    volume = pesoar - pesosub
    vetor_calculados.append(volume)                                 # VOLUME POS 0
    densidade_aparente = pesoar/volume
    vetor_calculados.append(densidade_aparente)                     # DENSIDADE APARENTE POS 1
    dados_coleta = bancodedadosnovo.get_leituraEnsaio(id_ensaio)
    leituraEnsaio = pos_curva(id_ensaio,1)
    fluencia, estabilidade = max(leituraEnsaio, key=lambda item: item[1])
    h = altura
    estabilidade_max = estabilidade*927.3*pow(h,-1.64)
    vetor_calculados.append(estabilidade_max)                       # ESTABILIDADE POS 2
    fluencia_max = fluencia
    vetor_calculados.append(fluencia_max)                           # FLUENCIA POS 3
    return vetor_calculados

def calcular_10794(pesosub, pesoar, temp, diametro, altura, asfato, id_ensaio):
    vetor_calculados =[]
    volume = pesoar - pesosub
    vetor_calculados.append(volume)                                 # VOLUME POS 0
    densidade_aparente = pesoar/volume
    vetor_calculados.append(densidade_aparente)                     # DENSIDADE APARENTE POS 1
    dados_coleta = bancodedadosnovo.get_leituraEnsaio(id_ensaio)
    leituraEnsaio = pos_curva(id_ensaio,1)
    fluencia, estabilidade = max(leituraEnsaio, key=lambda item: item[1])
    h = altura
    estabilidade_max = estabilidade*927.3*pow(h,-1.64)
    vetor_calculados.append(estabilidade_max)                       # ESTABILIDADE POS 2
    fluencia_max = fluencia
    vetor_calculados.append(fluencia_max)                           # FLUENCIA POS 3
    return vetor_calculados

def calcular_1362018(id_ensaio, D, H):
    vetor_calculados = []
    leituraEnsaio = pos_curva(id_ensaio,2)
    max_x, max_y = max(leituraEnsaio, key=lambda item: item[1])
    resistecia_tracao_indireta = 2*max_y*9.806/(math.pi*D*H)
    vetor_calculados.append(max_y)
    vetor_calculados.append(resistecia_tracao_indireta)
    return vetor_calculados

def pos_curva(id_ensaio, ensaio):
    dados_coleta = bancodedadosnovo.get_leituraEnsaio(id_ensaio)
    deformacao = []
    estabilidade = []
    for i in range((len(dados_coleta))):
        deformacao.append(dados_coleta[i][1])
        estabilidade.append(dados_coleta[i][2])
    estabilidade_mm = filtro_mm(estabilidade)
    deformacao_mm = offset(deformacao, estabilidade_mm)
    plt.clf()
    plt.plot(deformacao_mm, estabilidade_mm)
    plt.ylim(-0.05, 1.05*max(estabilidade_mm))
    plt.xlim(0, max(deformacao))
    if(ensaio == 1):
        plt.title('Ensaio de Compressao')
    elif(ensaio == 2):
        plt.title('Ensaio de Tracao')
    plt.ylabel('Forca, kgf')
    plt.xlabel('Deformacao, mm')
    plt.grid(True)
    print("Leitura id: ", id_ensaio)
    plt.savefig('graficos\E'+str(id_ensaio)+'.png', format='png')
    leituraEnsaio = []
    for i in range((len(estabilidade_mm))):
        vetor = []
        vetor.append(deformacao_mm[i])
        vetor.append(estabilidade_mm[i])
        leituraEnsaio.append(vetor)
    return leituraEnsaio

def filtro_mm(estabilidade):
    tam_grupo = 8
    i = 0
    medias_moveis=[]

    while i < len(estabilidade) - tam_grupo + 1:
        grupo = estabilidade[i : i + tam_grupo]
        media_grupo = sum(grupo) / tam_grupo
        medias_moveis.append(media_grupo)
        i +=1

    return medias_moveis

def offset(deformacao, estabilidade_mm):
    deformacao_mm = deformacao[3:-4]  #COMO FIZEMOS UMA MM DA ESTABILIDADE DE 8 PONTOS, PRECISAMOS TIRAR 4 PONTNOS INICIAIS E 4 PONTOS FINAIS DA DEFORMACAO
    soma = 0
    # for i in range(len(estabilidade_mm)):
    #     if(estabilidade_mm[i] > 24.0):
    #         pos = i
    #         break
    for i in range(45):
        soma += estabilidade_mm[i]
    media = soma/(45)
    for i in range(len(estabilidade_mm)):
        estabilidade_mm[i] = estabilidade_mm[i] - media
    pos = 0
    for i in range(len(estabilidade_mm)):
        if(estabilidade_mm[i] > 32.0):
            pos = i
            break
    deformacao_mm_new = []
    for i in range(len(deformacao_mm)):
        deformacao_mm_new.append(deformacao_mm[i] - deformacao_mm[pos-20])
    return deformacao_mm_new
