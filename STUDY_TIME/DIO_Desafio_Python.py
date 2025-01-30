# DIO 10/07/2024

# Desafio 1
# Calcular a média é uma das operações estatísticas mais básicas e úteis para resumir um conjunto de dados. 
# Dada uma lista de números, você deve calcular a média aritmética desses números.

# Receber a lista do usuário
entrada = input('Digite uma lista de valores: X, Y, Z')

# Convertee a string de entrada em uma lista de números
lista = [float(x.strip()) for x in entrada.split(',')]

# Calcula a soma dos números na lista
soma = sum(lista)

# Calcula a quantidade de elementos na lista
quantidade = len(lista)

#TO DO CALCULE A MEDIA
media = soma / quantidade

# Exibir a média com duas casas decimais
print('total elementos: ', quantidade)
print('Media {} / {} é igual a {}'.format(soma, quantidade, media))




#Desafio 2
#A mediana é uma medida de tendência central que é menos sensível a valores extremos do que a média. 
# Dada uma lista de números, você deve calcular a mediana.

# Define a função para calcular a mediana de uma lista de números
#Opções de input:
numeros = input("Digite uma lista de números separados por espaço: ")
numeros = list(map(float, numeros.split(',')))
#numeros = [10,20,30,40,50,80]

def calcular_mediana(numeros):
    # Ordena a lista de números em ordem crescente
    numeros_ordenados = sorted(numeros)
    # Obtém o comprimento da lista ordenada
    n = len(numeros_ordenados)
    # Calcula o ponto médio da lista
    ponto_medio = n // 2

    # TODO: Verifique se a quantidade de números é ímpar
    if n % 2 == 1:
    # Se for ímpar, retorna o valor no meio da lista
        return numeros_ordenados[ponto_medio]
    # Se for par, retorna a média dos dois valores do meio da lista
    else:
        media = (numeros_ordenados[ponto_medio] + numeros_ordenados[ponto_medio-1])/2
        return media

# Chama a função calcular_mediana com a lista de números como argumento e imprime o resultado
print(calcular_mediana(numeros))