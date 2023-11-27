from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from functions import save_options, select_source, test_and_save_image

def main():
    # Especifique o diretório de destino
    download_directory = r"C:\Users\joaos\Documents\SeleniumProjeto\images"  # Examplo: r"C:\Users\Maquinado\Documents\SeleniumProjeto\images"

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
    driver.get("http://isp.tools/traceroute")

    # Esperar um momento para o site carregar completamente
    time.sleep(5)

    # Extrair e salvar as opções de origem em um arquivo CSV
    opcoes_origem = save_options(driver)

    # Escolher uma origem e testar o IP
    selected_option = select_source(driver, opcoes_origem)
    if selected_option:
        test_and_save_image(driver, selected_option)

    # Fechar o navegador
    driver.quit()

if __name__ == '__main__':
    main()



#Pegar o ms e o hop