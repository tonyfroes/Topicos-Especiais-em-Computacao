from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import requests

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
    with open('ips.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Pular o cabeçalho, se houver

        for row in csv_reader:
            new_value = row[0]  # Assume que o IP está na primeira coluna

            driver.execute_script("document.getElementById('ip').value = arguments[0];", new_value)

            testar_button = driver.find_element(By.ID, "testar")
            if testar_button.is_enabled() and testar_button.is_displayed():
                testar_button.click()
                print("Botão Testar clicado!")

                try:
                    WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.ID, "graph_end")))
                    print("A tabela foi carregada com sucesso!")

                    salvar_png_button = WebDriverWait(driver, 120).until(
                        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Salvar PNG')]"))
                    )
                    if salvar_png_button.is_enabled() and salvar_png_button.is_displayed():
                        time.sleep(10)
                        salvar_png_button.click()
                        print("Botão 'Salvar PNG' clicado!")
                        time.sleep(5)
                    else:
                        print("Botão 'Salvar PNG' não disponível para clique.")
                except Exception as e:
                    print("A tabela não foi carregada após 30 segundos.")
            else:
                print("Botão Testar não disponível para clique.")

