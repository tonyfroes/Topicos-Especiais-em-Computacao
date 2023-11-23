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

                # Esperar até que o elemento <tfoot> com o ID "graph_end" seja exibido
                wait = WebDriverWait(driver, 120)
                wait.until(EC.visibility_of_element_located((By.ID, "graph_end")))

                # Esperar até que a tabela de resultados seja exibida
                result_table = wait.until(EC.visibility_of_element_located((By.ID, "graph_table")))

                # Esperar até que todas as linhas estejam presentes na tabela
                wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "tr")))
                
                # Esperar até que o elemento <tfoot> com o ID "graph_end" seja exibido
                wait.until(EC.presence_of_element_located((By.ID, "graph_end")))

                print("Tabela de resultados exibida!")
                # Encontrar todas as linhas na tabela
                rows = result_table.find_elements(By.TAG_NAME, "tr")[:-1]

                with open('traceroute.csv', 'a') as f:
                    hop_ms_list = []

                    for row in rows:
                        cells = row.find_elements(By.TAG_NAME, "td")
                        if cells:
                            
                            hop = cells[0].text
                            ms = cells[3].text if len(cells) > 3 else ""
                            if ms != "FIM":  # Salvar todos os valores exceto "FIM" na lista
                                print(f"{selected_option},{new_value},{hop},{ms}")
                                hop_ms_list.append(f"{selected_option},{new_value},{hop},{ms}\n")
                    
                    # Salvar todos os valores dos elementos 'td', exceto "FIM"
                    for line in hop_ms_list:
                        print("Ultimo appende")
                        f.write(line)
                    
                    # Salvar o valor do elemento 'th' com ID "graph_ms" no final
                    #ms_th_element = result_table.find_element(By.ID, "graph_ms")
                    #ms = ms_th_element.text
                    #f.write(f"{selected_option},{new_value},,{ms}\n")