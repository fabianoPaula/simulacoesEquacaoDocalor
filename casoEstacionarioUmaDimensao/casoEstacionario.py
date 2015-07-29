#!/usr/bin/env python
# coding=utf-8
import numpy as np
import scipy as sp
import scipy.sparse
import matplotlib.pyplot as plt
import Image

import sys 

# E preciso determinar os parmetros do problema
# Sãa eles:
# L = comprimento da barra
# n = número de intervalos
# T1 = temperatura na ponta esquerda
# T2 = temperatura na ponta direita

def usage():
     print('''Resolve o problema do calor no caso estacionário em 1-dimensão.  \n
Parâmetros Obrigatórios:
    -L  <Valor> - Comprimento da barra;
    -n  <Valor> - Número de espaços para a discretização;
    -T1 <Valor> - Temperatura na extremidade esquerda da barra;
    -T2 <Valor> - Temeperatura na extremidade direita da barra;
Parâmetros Opcionais:
    -sD <nome-do-arquivo> - Salva a discretização em arquivo
    -sR <nome-do-arquivo> - Salva o resultado em arquivo
    -sI <nome-do-arquivo> - Salva o gráfico em arquivo
    --noplot              - Não plota o gráfico
    --help                - exibe a ajuda''')
     exit()

def salvaVetor(nomearquivo,vetor,tam):
    arquivo = open(nomearquivo, "w")
    i = 0
    while( i < len(vetor)):
        arquivo.write("%f\n" % (vetor[i]))
        i = i + 1

list = sys.argv
i = 1
while( i < len(list)):
    if( list[i] == "--help"):
        usage()
    elif( list[i] == "-L"):
        L = float(list[i+1])
    elif( list[i] == "-T1"):
        T1 = float(list[i+1])
    elif( list[i] == "-T2"):
        T2 = float(list[i+1])
    elif( list[i] == "-n"):
        n = int(list[i+1])
    elif( list[i] == "-sD"):
        sD = list[i+1]
    elif( list[i] == "-sF"):
        sF = list[i+1]
    elif( list[i] == "-sI"):
        sI = list[i+1]
    elif( list[i] == "--noplot"):
        noplot = 1
        i = i + 1
        continue
    else:
        print("Argumento Inválido: "+list[i]+"")
        exit()
    i = i+2

if 'n' not in globals(): 
    usage()
if 'L' not in globals():
    usage()
if 'T1' not in globals():
    usage()
if 'T2' not in globals():
    usage()

print("Comprimento da Barra: %f" % (L))
print("Intervalos de discretização: %d" % (n))
print("Temperatura na extremidade a esquerda: %f" % (T1))
print("Temperatura na extremidade a direta: %f" % (T2))

h = L/n

x = np.zeros((n+1))
i = 1
while(i < (n+1)):
    x[i] = x[i-1] + h
    i = i + 1


# Está ceto dimensão n
A = np.zeros((n-1,n-1))
i = 0
while(i < (n-2)):
    A[i+1,i] = 1
    A[i,i] = -2
    A[i,i + 1] = 1
    i = i + 1
A[n-2,n-2] = -2

b = np.zeros((n-1))
b[0] = -T1
b[n-2] = -T2

y = np.linalg.solve(A,b)
y = np.append([T1],y)
y = np.append(y,[T2])

# para ver os gráficos corrtamente é preciso adicionar as condições de contorno

if 'sD' in globals():
    salvaVetor(sD,x,n+2)

if 'sF' in globals():
    salvaVetor(sF,y,n+2)

plt.plot(x,y,"g^")
if 'sI' in globals():
    plt.savefig(sI)
if 'noplot' not in globals():
    plt.show()
