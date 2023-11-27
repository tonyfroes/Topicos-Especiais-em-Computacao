import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Caminho do arquivo CSV
nome_do_arquivo = r'traceroute.csv'

# Carregando os dados do arquivo CSV, pulando a primeira linha
dados = pd.read_csv(nome_do_arquivo, skiprows=1, header=None, names=['Localizacao', 'IP', 'Hop', 'Tempo'])

# Removendo as linhas com 'unreachable' e a linha com o cabeçalho "Tempo (ms)"
dados = dados[(dados['Tempo'] != 'unreachable') & (dados['Tempo'] != 'Tempo (ms)')]

# Convertendo a coluna 'Tempo' para valores numéricos (removendo 'ms')
dados['Tempo'] = dados['Tempo'].str.rstrip('ms').astype(float)

# Agrupando os dados por IP e calculando a média do tempo
dados_agrupados = dados.groupby('IP')['Tempo'].mean().reset_index()

# Adicionando uma coluna com o ms esperado (calculado manualmente por você)
dados_agrupados['Esperado'] = [10, 15, 12, 15, 18, 21]  # Substitua com seus valores reais

# Criando um gráfico de barras
bar_width = 0.35
bar_positions = np.arange(len(dados_agrupados['IP']))

# Desenhando as barras do "Esperado" primeiro
plt.bar(bar_positions, dados_agrupados['Esperado'], width=bar_width, label='Esperado')

# Desenhando as barras do "Real" por cima
plt.bar(bar_positions, dados_agrupados['Tempo'], width=bar_width, label='Real', alpha=0.7)

# Adicionando rótulos e legendas
plt.xlabel('IP')
plt.ylabel('Tempo (ms)')
plt.title('Comparação de Tempo Real e Esperado por IP')
plt.xticks(bar_positions, dados_agrupados['IP'])
plt.legend()

# Exibindo o gráfico
plt.show()
