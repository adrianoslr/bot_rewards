import os
import os.path
import sys
import time

from lib.save_log import log
from pathlib import Path
from os.path import getmtime
from datetime import date, datetime

from dateutil.relativedelta import relativedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Defina os diretórios
ROOT_DIR = os.path.dirname(sys.modules["__main__"].__file__)
LOG_DIR = os.path.join(ROOT_DIR, "log")
DRIVER_DIR = os.path.join(ROOT_DIR, "bin")
logFile = os.path.join(LOG_DIR, f'{datetime.now().strftime("%Y%m%d%H%M%S")}.log')

# Lista de palavras
words = ("python", "casa", "boné", "fritas", "poney", "cachorro", "agua", "litro", "alho", "cebola",
         "cobaia", "sacola", "boina", "chute", "liquido", "podar", "ilha", "controle", "tetra", "sereno",
         "terra", "estrela", "buraco", "chicote", "pintor", "olho", "sono", "coelho", "pipa", "moto",
         "oito", "escola", "grego", "brasil", "espiao", "gibi", "castor", "campeao")

# Configura as variáveis de ambiente para o webdriver-manager
os.environ['WDM_LOCAL'] = '1'
os.environ['WDM_TARGET'] = DRIVER_DIR

def open_site():
    """Login and search in rewards"""
    driver_path = EdgeChromiumDriverManager().install()
    service = EdgeService(executable_path=driver_path)
    browser = webdriver.Edge(service=service)
    browser.maximize_window()
    browser.get('https://www.bing.com/news/?form=ml11z9&crea=ml11z9&wt.mc_id=ml11z9&rnoreward=1&rnoreward=1')
    time.sleep(5)
    cookie = browser.find_element(By.ID, "bnp_btn_accept")
    cookie.click()

    for word in words:
        if words.index(word) % 4 == 0 and words.index(word) != 0:
            log.debug("Starting waiting")
            time.sleep(900)
            log.debug("Waiting ok")
        element = browser.find_element(By.ID, 'sb_form_q')
        element.send_keys(word)
        search = browser.find_element(By.ID, 'sb_form_go')
        search.click()
        time.sleep(10)
        browser.get('https://www.bing.com/news/?form=ml11z9&crea=ml11z9&wt.mc_id=ml11z9&rnoreward=1&rnoreward=1')
        log.debug(f"Searching word {word}")
        time.sleep(5)

    browser.quit()
    log.debug("Closing program")

def clean_log():
    """Clean log directory"""
    log.debug("Deleting old logs")

    for file in Path(LOG_DIR).rglob("*"):
        if date.strftime(
            datetime.fromtimestamp(getmtime(file)),
            "%Y%m%d",
        ) < date.strftime(date.today() - relativedelta(days=30), "%Y%m%d"):
            file.unlink()

if __name__ == "__main__":
    clean_log()
    open_site()
