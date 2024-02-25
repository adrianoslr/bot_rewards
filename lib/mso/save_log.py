"""Log Capture Definition Module"""

# pylint: disable=line-too-long
import os
from datetime import datetime
import logging

from lib.constants import ROOT_DIR


LOG_DIR = os.path.join(ROOT_DIR, "log")
logFile = os.path.join(LOG_DIR, f'{datetime.now().strftime("%Y%m%d%H%M%S")}.log')


# Criamos o logger
# __name__ é uma variável que contem o nome do módulo. Assim, saberemos que módulo emitiu a mensagem
logger = logging.getLogger(__name__)
# apresentar apenas as mensagens de INFO e as inferiores (WARNING, ERROR, CRITICAL)
logger.setLevel(logging.DEBUG)
# se desejássemos registrar apenas ERROR e CRITICAL, seria logging.ERROR

# Criamos um handler para enviar as mensagens para um arquivo
logger_handler = logging.FileHandler(logFile, encoding="utf-8")
logger_handler.setLevel(logging.DEBUG)


# Especifique a formatação da mensagem
logger_formatter = logging.Formatter(
    "%(asctime)s :: %(levelname)s :: %(threadName)s :: %(filename)s :: %(funcName)s :: %(lineno)d :: %(message)s"
)


# Associe esta formatação ao  Handler
logger_handler.setFormatter(logger_formatter)

# Associe o Handler ao  Logger
logger.addHandler(logger_handler)
