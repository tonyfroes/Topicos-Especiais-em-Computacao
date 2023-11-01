from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def save_options(driver):
    select_element = Select(driver.find_element(By.ID, "origem"))
    opcoes_origem = [option.text for option in select_element.options]

    # Exibir as opções de origem
    for i, opcao in enumerate(opcoes_origem, start=1):
        print(f"{i}. {opcao}")

    # Save the options in a CSV file
    with open('opcoes_origem.csv', 'w') as f:
        for item in opcoes_origem:
            f.write("%s\n" % item)
    
    return opcoes_origem

def select_source(driver, opcoes_origem):
    escolha = int(input("Escolha uma origem pelo número: "))
    if 1 <= escolha <= len(opcoes_origem):
        # Selecionar a opção no site com base no índice escolhido
        select_element = Select(driver.find_element(By.ID, "origem"))
        select_element.select_by_index(escolha - 1)
        # Pode adicionar uma pausa para garantir que a seleção seja processada
        time.sleep(2)
        # Verificar se a opção foi selecionada corretamente
        opcao_selecionada = select_element.first_selected_option.text
        print(f"Você selecionou: {opcao_selecionada}")
        return opcao_selecionada
    else:
        print("Escolha inválida. Por favor, escolha um número válido.")
        return None

def test_and_save_image(driver, selected_option):
    # Novo valor que você deseja definir
    new_value = input("Digite um IP(179.189.148.120): ")
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
