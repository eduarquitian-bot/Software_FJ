"""Registro de eventos y errores en archivo (único uso de archivos del sistema)."""

import logging  # Módulo estándar de Python para registrar mensajes
import os       # Para construir rutas y crear la carpeta de logs

# Ruta del archivo de logs: carpeta "logs" junto a este archivo
RUTA_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "eventos.log")

# Logger propio de la aplicación
_logger = logging.getLogger("software_fj")


def configurar_logger(modo="a"):
    """Configura el archivo de log. modo='a' agrega; modo='w' lo reinicia."""
    # Se crea la carpeta de logs si no existe
    os.makedirs(os.path.dirname(RUTA_LOG), exist_ok=True)
    # Se cierran manejadores anteriores para no duplicar líneas
    for manejador in list(_logger.handlers):
        _logger.removeHandler(manejador)
        manejador.close()
    # Manejador que escribe en el archivo con codificación UTF-8
    manejador = logging.FileHandler(RUTA_LOG, mode=modo, encoding="utf-8")
    # Formato: fecha | nivel | mensaje
    manejador.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s"))
    _logger.addHandler(manejador)
    _logger.setLevel(logging.INFO)
    # Evita que los mensajes se impriman también por la consola raíz
    _logger.propagate = False


def _asegurar_configuracion():
    """Configura el logger automáticamente si aún no se hizo."""
    if not _logger.handlers:
        configurar_logger()


def registrar_evento(mensaje):
    """Registra un evento informativo."""
    _asegurar_configuracion()
    _logger.info(mensaje)


def registrar_error(mensaje, excepcion=None):
    """Registra un error; si la excepción tiene causa encadenada, también la anota."""
    _asegurar_configuracion()
    if excepcion is not None and excepcion.__cause__ is not None:
        # __cause__ contiene la excepción original (encadenamiento con "raise ... from")
        mensaje = f"{mensaje} | causa original: {type(excepcion.__cause__).__name__}: {excepcion.__cause__}"
    _logger.error(mensaje)
