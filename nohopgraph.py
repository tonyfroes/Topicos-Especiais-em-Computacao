import pandas as pd
import matplotlib.pyplot as plt

# Lê o arquivo CSV
column_names = ['Estado Origem', 'Cidade Origem', 'IP Origem', 'Cidade Destino', 'IP Destino', 'Distância', 'Ping Esperado', 'Ping Obtido', 'HOPs']
data = pd.read_csv('information.csv', names=column_names, header=0)

distancia = data['Distância']
ping_esperado = data['Ping Esperado']
ping_obtido = data['Ping Obtido']

plt.figure(figsize=(10, 6))

plt.scatter(distancia, ping_esperado, label='Ping Esperado', color='blue', alpha=0.7)
plt.scatter(distancia, ping_obtido, label='Ping Obtido', color='red', alpha=0.7)

plt.xlabel('Distância (km)')
plt.ylabel('Ping (ms)')
plt.title('Distância com Ping Esperado e Ping Obtido')
plt.legend()

# Mostra o gráfico
plt.grid(True)
plt.tight_layout()
plt.show()
