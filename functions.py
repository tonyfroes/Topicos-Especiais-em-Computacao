from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

def save_options(driver):
    select_element = Select(driver.find_element(By.ID, "origem"))
    opcoes_origem = [option.text for option in select_element.options]

    for i, opcao in enumerate(opcoes_origem, start=1):
        print(f"{i}. {opcao}")

    with open('opcoes_origem.csv', 'w') as f:
        for item in opcoes_origem:
            f.write("%s\n" % item)
    
    return opcoes_origem

def select_source(driver, opcoes_origem):
    escolha = int(input("Escolha uma origem pelo número: "))
    if 1 <= escolha <= len(opcoes_origem):
        select_element = Select(driver.find_element(By.ID, "origem"))
        select_element.select_by_index(escolha - 1)
        opcao_selecionada = select_element.first_selected_option.text
        print(f"Você selecionou: {opcao_selecionada}")
        return opcao_selecionada
    else:
        print("Escolha inválida. Por favor, escolha um número válido.")
        return None

def test_and_save_image(driver, selected_option):
    with open('ips.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)

        for row in csv_reader:
            new_value = row[0]

            driver.execute_script("document.getElementById('ip').value = arguments[0];", new_value)

            testar_button = driver.find_element(By.ID, "testar")
            if testar_button.is_enabled() and testar_button.is_displayed():
                testar_button.click()
                print("Botão Testar clicado!")

                wait = WebDriverWait(driver, 120)
                wait.until(EC.visibility_of_element_located((By.ID, "graph_end")))

                result_table = wait.until(EC.visibility_of_element_located((By.ID, "graph_table")))

                wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "tr")))
                
                wait.until(EC.presence_of_element_located((By.ID, "graph_end")))

                print("Tabela de resultados exibida!")
                rows = result_table.find_elements(By.TAG_NAME, "tr")[:-1]

                data_to_write = []

                for row in rows:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if cells:
                        hop = cells[0].text
                        ms = cells[3].text if len(cells) > 3 else ""
                        if ms != "FIM":
                            selected_option = selected_option
                            new_value = new_value

                            data_to_write.append([selected_option, new_value, hop, ms])
                    elif row.find_elements(By.TAG_NAME, "th"):
                        th_elements = row.find_elements(By.TAG_NAME, "th")
                        hop = th_elements[0].text
                        ms = th_elements[3].text
                        data_to_write.append([selected_option, new_value, hop, ms])
                        print("Cabeçalho da tabela encontrado!")
                csv_file = 'traceroute.csv'

                with open(csv_file, 'a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    
                    # Se o arquivo estiver vazio, adicione o cabeçalho
                    #if os.stat(csv_file).st_size == 0:
                        #writer.writerow(['selected_option', 'new_value', 'hop', 'ms'])  # Cabeçalho

                    # Escreve os dados na lista no arquivo CSV
                    writer.writerows(data_to_write)