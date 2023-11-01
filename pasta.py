from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Especifique o diretório de destino
download_directory = r"C:\Users\TonyFroes\Documents\SeleniumProjeto\images" # Examplo: r"C:\Users\Maquinado\Documents\SeleniumProjeto\images"

# Certifique-se de que o diretório de destino exista
if not os.path.exists(download_directory):
    os.makedirs(download_directory)

# Configurar as opções do Chrome para fazer o download no diretório especificado
chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": download_directory,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options.add_experimental_option("prefs", prefs)

# Inicializar o driver do Chrome com as opções personalizadas
driver = webdriver.Chrome(options=chrome_options)

# Navegar até o site
driver.get("http://www.isptools.com.br/mtr")

# Esperar um momento para o site carregar completamente
time.sleep(5)

# Encontrar o elemento <select> com base no ID "origem"
select_element = Select(driver.find_element(By.ID, "origem"))

# Extrair todas as opções de origem
opcoes_origem = [option.text for option in select_element.options]

# Exibir as opções de origem
for i, opcao in enumerate(opcoes_origem, start=1):
    print(f"{i}. {opcao}")

#Save the options in a csv file
with open('opcoes_origem.csv', 'w') as f:
    for item in opcoes_origem:
        f.write("%s\n" % item)


escolha = int(input("Escolha uma origem pelo número: "))

if 1 <= escolha <= len(opcoes_origem):
    # Selecionar a opção no site com base no índice escolhido
    select_element.select_by_index(escolha - 1)

    # Pode adicionar uma pausa para garantir que a seleção seja processada
    time.sleep(2)

    # Verificar se a opção foi selecionada corretamente
    opcao_selecionada = select_element.first_selected_option.text
    print(f"Você selecionou: {opcao_selecionada}")

    #save the selected option in a list selecionada = []
    selecionada = []
    selecionada.append(opcao_selecionada)
    print(selecionada)

    # Novo valor que você deseja definir
    new_value = input("Digite um IP(179.189.148.120): ")
    print("Exemplo de IP: 179.189.148.120")
    #new_value = "179.189.148.120"


    # Execute um script JavaScript para definir o novo valor
    driver.execute_script("document.getElementById('ip').value = arguments[0];", new_value)

    # Localize o botão "Testar" e clique nele
    testar_button = driver.find_element(By.ID, "testar")
    if testar_button.is_enabled() and testar_button.is_displayed():
        testar_button.click()
        print("Botão Testar clicado!")

        # Aguarde até que a tabela termine de carregar
        try:
            WebDriverWait(driver, 100).until(
                EC.visibility_of_element_located((By.ID, "graph_end"))
            )
            print("A tabela foi carregada com sucesso!")

            # Localize o botão "Salvar PNG" e clique nele
            salvar_png_button = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Salvar PNG')]"))
            )
            if salvar_png_button.is_enabled() and salvar_png_button.is_displayed():
                time.sleep(10)
                salvar_png_button.click()
                print("Botão 'Salvar PNG' clicado!")

                # Aguarde um momento (por exemplo, 5 segundos) para o download
                time.sleep(5)
            else:
                print("Botão 'Salvar PNG' não disponível para clique.")
        except Exception as e:
            print("A tabela não foi carregada após 30 segundos.")
    else:
        print("Botão Testar não disponível para clique.")
else:
    print("Escolha inválida. Por favor, escolha um número válido.")

# Fechar o navegador
driver.quit()
