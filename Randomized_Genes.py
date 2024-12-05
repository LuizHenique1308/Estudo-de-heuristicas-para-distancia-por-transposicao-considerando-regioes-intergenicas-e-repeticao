import numpy as np  # Importa a biblioteca NumPy para geração de números aleatórios e operações com arrays
import time

start_time = time.time()  # Marca o tempo inicial

def ler_arquivo(arquivo_entrada):
    """
    Lê o arquivo de entrada e retorna uma lista com as linhas do arquivo.
    """
    with open(arquivo_entrada, 'r') as arquivo:
        linhas = arquivo.readlines()
    return linhas


def contar_repeticoes(numeros):
    """
    Conta quantas vezes cada gene aparece em uma lista de números e retorna um dicionário
    com os genes repetidos e suas quantidades.
    """
    return {gene: numeros.count(gene) for gene in set(numeros) if numeros.count(gene) > 1}


def gerar_vetores_aleatorios(linha1):
    """
    Gera vetores aleatórios para substituir genes repetidos, garantindo que um dos valores seja o gene original.
    """
    vetores_aleatorios = {}
    valor_maximo_atual = max(linha1)  # Define o maior valor atual para garantir unicidade


    repeticoes_da_linha = contar_repeticoes(linha1)
    for gene, quantidade in repeticoes_da_linha.items():
            if gene not in vetores_aleatorios:
                valores_aleatorios = np.random.permutation(np.arange(valor_maximo_atual + 1, valor_maximo_atual + quantidade))
                vetor_aleatorio = np.append(valores_aleatorios, gene)
                vetores_aleatorios[gene] = vetor_aleatorio
                #print(f"Vetores aleatórios para o gene {gene}: {vetor_aleatorio}")
                valor_maximo_atual += quantidade - 1
    return vetores_aleatorios


def substituir_repeticoes_com_vetor(numeros, vetores_aleatorios):
    """
    Substitui os genes repetidos em uma lista pelos valores de seus vetores aleatórios.
    """
    # Embaralha os vetores de valores aleatórios para cada gene
    for gene in vetores_aleatorios:
        np.random.shuffle(vetores_aleatorios[gene])  # Embaralha o vetor de cada gene

    #print(f"Vetores aleatórios após embaralhamento: {vetores_aleatorios}")

    # Contador para controlar a substituição de cada gene
    contador_genes = {gene: 0 for gene in vetores_aleatorios}
    #print(f"Contador de genes: {contador_genes}")

    # Lista para armazenar os novos números (com as substituições)
    novos_numeros = []


    for gene in numeros:
        #print('gene = ', gene)
        if gene in vetores_aleatorios:
            #print('vetores_aleatorios = ', vetores_aleatorios)
            novo_valor = vetores_aleatorios[gene][contador_genes[gene]]
            #print('novo_valor = ', novo_valor)

            novos_numeros.append(novo_valor)
            contador_genes[gene] += 1
        else:
            novos_numeros.append(gene)  # Mantém os genes que não são repetidos

    return novos_numeros


def processar_bloco(linha1, linha2, linha3, linha4, vetores_aleatorios):
    """
    Processa um bloco de 4 linhas, substituindo genes repetidos pelas versões mapeadas aleatoriamente.
    """
    linha1_mapeada = substituir_repeticoes_com_vetor(linha1, vetores_aleatorios)
    linha3_mapeada = substituir_repeticoes_com_vetor(linha3, vetores_aleatorios)

    return [
        ' '.join(map(str, linha1_mapeada)) + '\n',
        linha2 + '\n',
        ' '.join(map(str, linha3_mapeada)) + '\n',
        linha4 + '\n'
    ]

def extrair_linhas_do_bloco(linhas):
    """
    Extrai e processa um bloco de 4 linhas do arquivo de entrada.
    """
    linha1 = list(map(int, linhas[0].strip().split()))  # Primeira linha (genes)
    linha2 = linhas[1].strip()  # Segunda linha (não alterada)
    linha3 = list(map(int, linhas[2].strip().split()))  # Terceira linha (genes)
    linha4 = linhas[3].strip()  # Quarta linha (não alterada)

    return linha1, linha2, linha3, linha4


def processar_arquivo_com_vetores_aleatorios(arquivo_entrada):
    """
    Processa um arquivo de entrada com conjuntos de 4 linhas, substituindo genes repetidos
    por valores aleatórios exclusivos.
    Retorna as linhas processadas.
    """
    # Lê o arquivo de entrada
    linhas = ler_arquivo(arquivo_entrada)

    # Inicializa uma lista para armazenar as linhas processadas
    linhas_processadas = []

    # Extrai as 4 linhas do da entrada
    linha1, linha2, linha3, linha4 = extrair_linhas_do_bloco(linhas)

    # Gera o mapeamento de genes para vetores aleatórios
    vetores_aleatorios = gerar_vetores_aleatorios(linha1)

    # Processa o bloco de 4 linhas
    bloco_processado = processar_bloco(linha1, linha2, linha3, linha4, vetores_aleatorios)

    # Adiciona o bloco processado à lista de saída
    linhas_processadas.extend(bloco_processado)

    return linhas_processadas


def salvar_ou_imprimir(linhas_processadas, arquivo_saida=None):
    """
    Salva as linhas processadas em um arquivo ou imprime no terminal.
    Se um arquivo de saída for especificado, escreve no arquivo.
    Caso contrário, imprime as linhas no terminal.
    """
    if arquivo_saida:
        with open(arquivo_saida, 'w') as arquivo:
            arquivo.writelines(linhas_processadas)
    else:
        # Caso contrário, imprime as linhas processadas no terminal
        for linha in linhas_processadas:
            print(linha.strip())


# Exemplo de uso:
arquivo_entrada = 'input.txt'  # Caminho do arquivo de entrada
arquivo_saida = None  # Se não especificado, a saída será exibida no terminal

#for i in range(50):
#    start_time = time.time()  # Marca o tempo inicial
#    linhas_processadas = processar_arquivo_com_vetores_aleatorios(arquivo_entrada)
#    salvar_ou_imprimir(linhas_processadas, arquivo_saida)
    # Calcula e exibe o tempo total de execução
#    end_time = time.time()  # Marca o tempo final
#    execution_time = end_time - start_time
#    minutes, seconds = divmod(execution_time, 60)
#    print(f"Tempo de execução: {execution_time:.4f} segundos OU {int(minutes)} minutos e {seconds:.4f} segundos")
    #print('\n')

# Chama a função principal e obtém as linhas processadas
linhas_processadas = processar_arquivo_com_vetores_aleatorios(arquivo_entrada)

# Chama a função para salvar no arquivo ou imprimir no terminal
salvar_ou_imprimir(linhas_processadas, arquivo_saida)

# Calcula e exibe o tempo total de execução
end_time = time.time()  # Marca o tempo final
execution_time = end_time - start_time
minutes, seconds = divmod(execution_time, 60)
print(f"Tempo de execução: {execution_time:.4f} segundos OU {int(minutes)} minutos e {seconds:.4f} segundos")