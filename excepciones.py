"""Excepciones personalizadas del sistema Software FJ.

Todas heredan de SoftwareFJError, de modo que el sistema pueda capturar
cualquier error propio con un solo ``except SoftwareFJError`` y, aun así,
distinguir cada situación con una clase específica.
"""


class SoftwareFJError(Exception):
    """Excepción base de la aplicación."""

    def __init__(self, mensaje, codigo="FJ-000"):
        # Se envía el mensaje a la clase padre para conservar el comportamiento estándar
        super().__init__(mensaje)
        # Se guardan el mensaje y un código para facilitar la lectura del log
        self.mensaje = mensaje
        self.codigo = codigo

    def __str__(self):
        # Representación en texto: [CÓDIGO] mensaje
        return f"[{self.codigo}] {self.mensaje}"


class DatoInvalidoError(SoftwareFJError):
    """Se lanza cuando un dato tiene un formato o valor incorrecto."""

    def __init__(self, mensaje):
        super().__init__(mensaje, "FJ-001")


class ParametroFaltanteError(SoftwareFJError):
    """Se lanza cuando falta un parámetro obligatorio."""

    def __init__(self, mensaje):
        super().__init__(mensaje, "FJ-002")


class OperacionNoPermitidaError(SoftwareFJError):
    """Se lanza cuando se intenta una operación que el estado actual no permite."""

    def __init__(self, mensaje):
        super().__init__(mensaje, "FJ-003")


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando se intenta usar un servicio que no está disponible."""

    def __init__(self, mensaje):
        super().__init__(mensaje, "FJ-004")


class ReservaError(SoftwareFJError):
    """Se lanza cuando una reserva no puede crearse o gestionarse."""

    def __init__(self, mensaje):
        super().__init__(mensaje, "FJ-005")


class CalculoInconsistenteError(SoftwareFJError):
    """Se lanza cuando un cálculo de costos produce o recibe valores inconsistentes."""

    def __init__(self, mensaje):
        super().__init__(mensaje, "FJ-006")
