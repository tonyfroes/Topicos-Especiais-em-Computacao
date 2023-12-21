import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Substitua 'caminho/do/seu/arquivo.csv' pelo caminho real do seu arquivo CSV
caminho_arquivo_csv = 'information.csv'

# Carregando os dados do CSV
dados = pd.read_csv(caminho_arquivo_csv)

# Calculando a média dos pings obtidos por estado
media_ping_por_estado = dados.groupby(dados.columns[0])[dados.columns[7]].mean().reset_index()

# Criando um scatter plot com estado no eixo x e média do ping obtido no eixo y
plt.figure(figsize=(12, 8))
sns.scatterplot(x=media_ping_por_estado.columns[0], y=dados.columns[7], data=media_ping_por_estado, color='red', label='Média Ping Obtido', s=100)

# Adicionando rótulos e título
plt.title('Média dos Pings Obtidos por Estado')
plt.xlabel('Estado')
plt.ylabel(f'Média Ping Obtido (ms)')

# Exibindo o gráfico
plt.xticks(rotation=45)  # Rotaciona os rótulos do eixo x para melhor visualização
plt.grid(True)
plt.legend()
plt.show()