import time
start_time = time.time()  # Marca o tempo inicial

def montar_genoma(genes, regioes):
    """
    Monta o genoma intercalando genes e regiões intergênicas.
    Se o número de genes for igual ao número de regiões, começa com gene.
    Se houver mais regiões, começa com uma região intergênica.
    """
    genoma = []

    # Caso 1: Começa com gene se número de genes igual ao número de regiões
    if len(genes) == len(regioes):
        for gene, regiao in zip(genes, regioes):
            genoma.append(gene)
            genoma.append(regiao)

    # Caso 2: Começa com uma região se houver mais regiões do que genes
    elif len(regioes) > len(genes):
        genoma.append(regioes[0])  # Começa com a primeira região intergênica
        for gene, regiao in zip(genes, regioes[1:]):
            genoma.append(gene)
            genoma.append(regiao)

    # Se houver mais genes que regiões, adiciona o último gene no final
    if len(genes) > len(regioes):
        genoma.append(genes[-1])

    return genoma


def is_valid_subgenoma(i, j, genoma, genes, regioes):
    """
    Verifica se um subgenoma especificado atende às condições:
    - Deve começar com um gene e terminar com um gene.
    - Deve ter 3 elementos.
    Retorna True se as condições forem atendidas, caso contrário, False.
    """
    # O subgenoma deve ter 3 elementos
    if (j - i) != 3:
        return False

    # Verifica se o subgenoma começa com um gene e termina com um gene
    if len(genes) == len(regioes):
        #print('len(genes) == len(regioes)')
        # Se o número de genes é igual ao número de regiões
        return i % 2 == 0 and j % 2 == 1  # (começo com gene, fim com gene)
    else:
        # Se o número de genes é diferente
        return i % 2 == 1 and j % 2 == 0  # (começo com gene, fim com gene)

def encontrar_subgenoma_comum(genoma1, genoma2, genes1, regioes1, genes2, regioes2, subgenomas_encontrados):
    """
    Encontra todos os subgenomas comuns entre genoma1 e genoma2, com tamanho fixo de 3,
    que ainda não foram registrados como encontrados.
    """
    subgenoma_comum = None
    start1, end1, start2, end2 = -1, -1, -1, -1
    tamanho_subgenoma = 3
    subgenomas_genoma1 = {}
    subgenomas_armazenados = {}

    # Conjunto para armazenar genes já encontrados
    genes_encontrados = set()

    for i in range(len(genoma1) - tamanho_subgenoma + 1):
        subgenoma = tuple(genoma1[i:i + tamanho_subgenoma])
        if (is_valid_subgenoma(i, i + tamanho_subgenoma, genoma1, genes1, regioes1)
                and subgenoma not in subgenomas_encontrados):
            subgenomas_genoma1[subgenoma] = (i, i + tamanho_subgenoma)

    subgenomas_para_remover = []

    for subgenoma, (start1_genoma1, end1_genoma1) in subgenomas_genoma1.items():
        # Obter os genes iniciais e finais do subgenoma
        gene_inicial = genoma1[start1_genoma1]
        gene_final = genoma1[end1_genoma1 - 1]  # O último gene é o anterior ao final

        # Verifica se o gene inicial ou final já foi encontrado
        if gene_inicial in genes_encontrados or gene_final in genes_encontrados:
            continue  # Se já encontrado, pula para o próximo subgenoma

        for k in range(len(genoma2) - tamanho_subgenoma + 1):
            if tuple(genoma2[k:k + tamanho_subgenoma]) == subgenoma:
                subgenoma_comum = subgenoma
                start2, end2 = k, k + tamanho_subgenoma
                start1, end1 = start1_genoma1, end1_genoma1

                # Armazena o subgenoma encontrado no dicionário
                subgenomas_armazenados[subgenoma] = (start1, end1, start2, end2)

                # Adiciona os genes inicial e final ao conjunto de genes encontrados
                genes_encontrados.add(gene_inicial)
                genes_encontrados.add(gene_final)

                break

    return subgenoma_comum, start1, end1, start2, end2, subgenomas_armazenados


def encapsular_subgenoma(genoma1, genoma2, start1, start2, subgenoma):
    """
    Altera o nome do subgenoma comum em genoma1 e genoma2 para o próximo número maior
    ainda não existente nos genes. Não move o subgenoma, apenas renomeia os genes encontrados.
    """
    # Filtrar apenas os genes (números inteiros) em genoma1 e genoma2
    genes1 = [gene for gene in genoma1 if isinstance(gene, int)]
    genes2 = [gene for gene in genoma2 if isinstance(gene, int)]

    if  genoma1[start1:start1+3] != genoma2[start2:start2+3]:
        raise ValueError("Os subgenomas não correspondem.")

    # Encontrar o próximo número maior não existente nos genes
    max_num = max(max(genes1), max(genes2)) + 1  # Próximo número maior
    subgenoma_max_num = [max_num]

    del genoma1[start1:start1 + len(subgenoma)]
    del genoma2[start2:start2 + len(subgenoma)]

    # Substituir o subgenoma por max_num em ambos os genomas
    genoma1[start1:start1] = subgenoma_max_num
    genoma2[start2:start2] = subgenoma_max_num

    return genoma1, genoma2


def intercalar_genoma(genes, regioes):
    """
    Intercala os genes e as regiões intergênicas de acordo com as regras:
    - Se o número de genes for igual ao número de regiões intergênicas, começa com gene.
    - Caso contrário, começa com a região intergênica.
    Retorna uma lista com o genoma intercalado.
    """
    genoma_intercalado = []

    if len(genes) == len(regioes):
        for gene, regiao in zip(genes, regioes):
            genoma_intercalado.append(gene)
            genoma_intercalado.append(regiao)
    elif len(genes) > len(regioes):
        for gene, regiao in zip(genes[:-1], regioes):
            genoma_intercalado.append(gene)
            genoma_intercalado.append(regiao)
        genoma_intercalado.append(genes[-1])  # Adiciona o último gene
    else:
        genoma_intercalado.append(regioes[0])
        for gene, regiao in zip(genes, regioes[1:]):
            genoma_intercalado.append(gene)
            genoma_intercalado.append(regiao)

    return genoma_intercalado


def processar_genomas(genes1, regioes1, genes2, regioes2):
    genoma1 = intercalar_genoma(genes1, regioes1)
    genoma2 = intercalar_genoma(genes2, regioes2)

    subgenomas_encontrados = set()
    movimentos = 0
    z = 0
    todos_subgenomas = {}  # Novo dicionário para armazenar todos os subgenomas encontrados

    while True:
        z += 1
        subgenoma, start1, end1, start2, end2, subgenomas_atualizados = encontrar_subgenoma_comum(
            genoma1, genoma2, genes1, regioes1, genes2, regioes2, subgenomas_encontrados
        )
        #print('subgenoma[', z, '] = ', subgenoma)

        if subgenoma:
            #print(f"Movendo subgenoma: {subgenoma}")
            encapsular_subgenoma(genoma1, genoma2, start1, start2, subgenoma)
            subgenomas_encontrados.add(subgenoma)
            todos_subgenomas.update(subgenomas_atualizados)  # Atualiza o dicionário com os subgenomas encontrados
            movimentos += 1
        else:
            print("Nenhum novo subgenoma comum encontrado. Encerrando.")
            break

    return genoma1, genoma2, todos_subgenomas  # Retorna também todos os subgenomas encontrados



def dividir_genoma_em_linhas(genoma):
    """
    Divide um genoma completo em suas respectivas linhas de genes e regiões intergênicas.
    Retorna duas listas: uma de genes e outra de regiões intergênicas.
    """
    genes = []
    regioes = []

    if isinstance(genoma[0], str):  # Caso o genoma comece com uma região intergênica
        regioes.append(genoma[0])
        genoma = genoma[1:]

    for i in range(0, len(genoma) - 1, 2):
        genes.append(genoma[i])
        regioes.append(genoma[i + 1])

    if len(genoma) % 2 != 0:
        genes.append(genoma[-1])  # Caso haja um gene sobrando

    return genes, regioes

def exibir_e_escrever_saida(output_file, genoma1, genoma2):
    """
    Exibe a saída no terminal e escreve os resultados em um arquivo de saída.
    Divide os genomas em genes e regiões intergênicas.
    """
    genes1, regioes1 = dividir_genoma_em_linhas(genoma1)
    genes2, regioes2 = dividir_genoma_em_linhas(genoma2)

    # Exibe no terminal
    print(' '.join(map(str, genes1)))  # Exibe genes do primeiro genoma
    print(' '.join(map(str, regioes1)))  # Exibe regiões intergênicas do primeiro genoma
    print(' '.join(map(str, genes2)))  # Exibe genes do segundo genoma
    print(' '.join(map(str, regioes2)))  # Exibe regiões intergênicas do segundo genoma

    # Escreve no arquivo de saída
    with open(output_file, 'w') as f:
        f.write(' '.join(map(str, genes1)) + '\n')
        f.write(' '.join(map(str, regioes1)) + '\n')
        f.write(' '.join(map(str, genes2)) + '\n')
        f.write(' '.join(map(str, regioes2)) + '\n')


def ler_arquivo_entrada(input_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    genes1 = list(map(int, lines[0].strip().split()))
    regioes1 = lines[1].strip().split()
    genes2 = list(map(int, lines[2].strip().split()))
    regioes2 = lines[3].strip().split()

    return genes1, regioes1, genes2, regioes2

# Exemplo de uso

input_file = 'input.txt'  # Caminho do arquivo de entrada
output_file = 'saida.txt'  # Caminho do arquivo de saída

# Lê os genomas do arquivo de entrada
genes1, regioes1, genes2, regioes2 = ler_arquivo_entrada(input_file)

# Processa os genomas para alinhar subgenomas comuns
genoma1, genoma2, todos_subgenomas = processar_genomas(genes1, regioes1, genes2, regioes2)

# Exibe a saída no terminal e salva em arquivo
exibir_e_escrever_saida(output_file, genoma1, genoma2)

print(f"Genomas processados e salvos no arquivo: {output_file}")

# Calcula e exibe o tempo total de execução
end_time = time.time()  # Marca o tempo final
execution_time = end_time - start_time
minutes, seconds = divmod(execution_time, 60)
print(f"Tempo de execução: {execution_time:.4f} segundos OU {int(minutes)} minutos e {seconds:.4f} segundos")