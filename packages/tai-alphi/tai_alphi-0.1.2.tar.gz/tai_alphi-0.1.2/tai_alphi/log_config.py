import logging

# Definición de colores
GREY = "\x1b[38;20m"
BLUE = "\033[94m"
YELLOW = "\x1b[33;20m"
RED = "\x1b[31;20m"
BOLD_RED = "\x1b[31;1m"
BOLD_PURPLE = "\x1b[36;1m"
RESET = "\x1b[0m"

# Formato de logging
BASE_FORMAT = "[%(asctime)s][%(levelname)s] %(message)s"
DEV_FORMAT = f"{BOLD_PURPLE}[%(mode)s]{RESET}"

# Diccionario de formatos
FORMATS = {
    logging.DEBUG: GREY + BASE_FORMAT + RESET,
    logging.INFO: BLUE + BASE_FORMAT + RESET,
    logging.WARNING: YELLOW + BASE_FORMAT + RESET,
    logging.ERROR: RED + BASE_FORMAT + RESET,
    logging.CRITICAL: BOLD_RED + BASE_FORMAT + RESET,
}

def update_formats_for_dev_mode():
    """
    Actualiza los formatos de logging para el modo de desarrollo.
    """
    for level in FORMATS:
        FORMATS[level] = DEV_FORMAT + FORMATS[level]
