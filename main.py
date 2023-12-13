import time
import os
from functions import save_options, select_source, test_dados
from selenium import webdriver

def main():
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://isp.tools/traceroute")
    time.sleep(5)
    opcoes_origem = save_options(driver)  # Salvar as opções de origem em um arquivo CSV

    for i in range(len(opcoes_origem)):
        selected_option = select_source(driver, opcoes_origem, i)
        if selected_option:
            print(selected_option)
            test_dados(driver, selected_option)
    
    driver.quit()

if __name__ == '__main__':
    main()
