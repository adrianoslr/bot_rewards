import os
import os.path
import sys
import time
import random

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

# Lista de palavras comuns em português
common_words = [
    "amor", "casa", "sol", "livro", "carro", "flor", "mar", "lua", "tempo", "cidade",
    "amizade", "paz", "sonho", "música", "dia", "noite", "luz", "rio", "céu", "estrela",
    "natureza", "coração", "vida", "ar", "vento", "terra", "caminho", "olho", "sorriso", "abraço",
    "python", "casa", "boné", "fritas", "poney", "cachorro", "agua", "litro", "alho", "cebola", 
    "cobaia", "sacola", "boina", "chute", "liquido", "podar", "ilha", "controle", "tetra", "sereno", 
    "terra", "estrela", "buraco", "chicote", "pintor", "olho", "sono", "coelho", "pipa", "moto", "oito", 
    "escola", "grego", "brasil", "espiao", "gibi", "castor", "campeao","amor", "amigo", "árvore", 
    "azul", "bebê", "beleza", "bicicleta", "bola", "bom", "brincadeira", "casa", "cachoeira", "café", 
    "calor", "cama", "cantar", "carro", "chuva", "cidade", "claridade", "comida", "coração", "correr", 
    "criança", "destino", "dia", "doce", "escola", "estrela", "estudar", "família", "felicidade", "festa", 
    "flor", "força", "frio", "fruta", "futuro", "garrafa", "geladeira", "girassol", "gato", "graça", 
    "homem", "horário", "igreja", "infinito", "infância", "janela", "jardim", "jovem", "jogo", "lágrima", 
    "liberdade", "livro", "lua", "mãe", "mar", "médico", "menina", "menino", "mesa", "mundo", "música", 
    "natureza", "noite", "olho", "ouro", "pai", "palavra", "papel", "passarinho", "paz", "pessoa", 
    "pintura", "planta", "praia", "prateado", "presente", "primavera", "professor", "praia", "quarto", 
    "quintal", "rapaz", "riso", "rosa", "saúde", "saudade", "semana", "senhor", "sonho", "sorte", "sorriso", 
    "tarde", "telefone", "tempo", "toalha", "trabalho", "trevo", "triste", "universo", "ursinho",
    "vassoura", "ventania", "verde", "verão", "viagem", "vida", "violão", "vista", "vontade", "voz", 
    "xícara", "zebra", "abacaxi", "aprender", "alcançar", "alegria", "abelha", "avião", "aquecimento", 
    "areia", "atualizar", "avenida", "bailarina", "bancário", "barulho", "beleza", "bezerro", "brilhante", 
    "cabelo", "caderno", "calculadora", "cachorro", "calçado", "caminhão", "campo", "cantar", "cavalo", 
    "cebola", "celular", "centavo", "cereja", "cimento", "cinto", "cidade", "cinema", "coração", "colher", 
    "computador", "conselho", "continuar", "coração", "correr", "curso", "data", "decidir", "dedicar", "dever", 
    "dez", "dirigir", "doce", "documento", "dúvida", "elefante", "energia", "entender", "envelope", "errar", 
    "estrela", "estrada", "estudar", "evento", "existir", "explicar", "fábrica", "faca", "fazer", "feliz", "férias", 
    "ferver", "fogo", "folha", "forma", "frio", "frutas", "garfo", "gente", "girafa", "goiaba", "grande", "gravata", 
    "guarda", "guerreiro", "habilitar", "habitar", "harmonia", "helicóptero", "história", "humano", "imagem", "imenso", 
    "importar", "indicar", "iniciar", "instantâneo", "interferir", "invadir", "inventar", "jarro", "jardim", "jogador", 
    "joelho", "jornal", "juvenil", "kiwi", "labirinto", "lâmpada", "lanterna", "lápis", "leitura", "liberar", "libra", 
    "limitar", "lixeira", "lilás", "lousa", "macaco", "maçã", "madeira", "mancha", "mão", "marido", "marca", "marrom", 
    "massa", "meditação", "melhor", "mentir", "menino", "mental", "mergulho", "mesa", "mistério", "moda", "monstro", 
    "mosca", "moto", "nadar", "nariz", "natal", "navegar", "negativo", "nome", "noite", "novela", "número", "objetivo", 
    "observador", "ouvir", "paz", "pedra", "pintar", "plantar", "ponte", "ponto", "popular", "porco", "positivo", 
    "prazo", "pressão", "primavera", "prova", "quente", "razão", "real", "rever", "rio", "risco", "roupa", "sabor", 
    "seguro", "sinal", "sonho", "sorte", "sussurro", "tatuagem", "teatro", "telefone", "tempero", "terno", "tesouro", 
    "tinta", "tique", "toalha", "treinar", "trabalho", "trovão"
]

# Função para gerar palavras aleatórias que façam sentido
def random_words(quantity):
    return random.sample(common_words, quantity)

# Lista de palavras aleatórias
words = random_words(30)

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
