"""Clase Reserva: integra cliente, servicio, duración y estado."""

from enum import Enum

from cliente import Cliente
from entidad_base import EntidadBase
from excepciones import (CalculoInconsistenteError, DatoInvalidoError,
                         OperacionNoPermitidaError, ReservaError,
                         ServicioNoDisponibleError, SoftwareFJError)
from logger import registrar_evento
from servicio import Servicio


class EstadoReserva(Enum):
    """Estados posibles de una reserva."""
    PENDIENTE = "pendiente"
    CONFIRMADA = "confirmada"
    CANCELADA = "cancelada"
    PROCESADA = "procesada"


class Reserva(EntidadBase):
    """Reserva de un servicio por parte de un cliente."""

    def __init__(self, cliente, servicio, duracion_horas, **parametros):
        super().__init__()
        # Validación de tipos de los objetos asociados
        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("La reserva requiere un Cliente válido.")
        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("La reserva requiere un Servicio válido.")
        # Conversión de la duración; si falla, se encadena la excepción original
        try:
            duracion = float(duracion_horas)
        except (TypeError, ValueError) as error:
            raise DatoInvalidoError(f"Duración no numérica: {duracion_horas!r}.") from error
        if not 0 < duracion <= 24:
            raise DatoInvalidoError(f"La duración debe estar entre 0 y 24 horas (recibido {duracion}).")
        # El servicio debe estar disponible
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{servicio.nombre}' no está disponible.")
        # Se validan los parámetros propios del servicio y se encadena el error si falla
        try:
            servicio.validar_parametros(**parametros)
        except SoftwareFJError as error:
            raise ReservaError(f"No se pudo crear la reserva de '{servicio.nombre}'.") from error
        # Atributos privados (encapsulación)
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__parametros = parametros
        self.__estado = EstadoReserva.PENDIENTE
        self.__costo_final = None

    # ---- propiedades de solo lectura ----
    @property
    def cliente(self):
        return self.__cliente

    @property
    def servicio(self):
        return self.__servicio

    @property
    def duracion(self):
        return self.__duracion

    @property
    def estado(self):
        return self.__estado

    @property
    def costo_final(self):
        return self.__costo_final

    # ---- operaciones ----
    def confirmar(self):
        """Pasa de PENDIENTE a CONFIRMADA."""
        if self.__estado is not EstadoReserva.PENDIENTE:
            raise OperacionNoPermitidaError(
                f"Reserva #{self.id}: no se puede confirmar en estado '{self.__estado.value}'.")
        if not self.__servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self.__servicio.nombre}' ya no está disponible.")
        self.__estado = EstadoReserva.CONFIRMADA
        registrar_evento(f"Reserva #{self.id} confirmada.")

    def cancelar(self):
        """Cancela la reserva si aún no fue procesada ni cancelada."""
        if self.__estado in (EstadoReserva.CANCELADA, EstadoReserva.PROCESADA):
            raise OperacionNoPermitidaError(
                f"Reserva #{self.id}: no se puede cancelar en estado '{self.__estado.value}'.")
        self.__estado = EstadoReserva.CANCELADA
        registrar_evento(f"Reserva #{self.id} cancelada.")

    def procesar(self, impuesto=None, descuento=None):
        """Calcula el costo final y marca la reserva como PROCESADA (solo si está CONFIRMADA)."""
        if self.__estado is not EstadoReserva.CONFIRMADA:
            raise OperacionNoPermitidaError(
                f"Reserva #{self.id}: debe estar confirmada para procesarse (estado '{self.__estado.value}').")
        try:
            # Intento de cálculo con las variantes de costo
            costo = self.__servicio.calcular_costo_total(self.__duracion, impuesto, descuento)
        except SoftwareFJError as error:
            # Se encadena el error original dentro de uno de más alto nivel
            raise CalculoInconsistenteError(f"Reserva #{self.id}: no se pudo calcular el costo.") from error
        else:
            # Solo si no hubo error se actualiza el estado
            self.__costo_final = costo
            self.__estado = EstadoReserva.PROCESADA
            return costo
        finally:
            # Se ejecuta siempre, haya o no error
            registrar_evento(f"Intento de procesar la reserva #{self.id} finalizado.")

    def describir(self):
        costo = f"${self.__costo_final:,.2f}" if self.__costo_final is not None else "sin calcular"
        return (f"Reserva #{self.id} | {self.__cliente.nombre} | {self.__servicio.nombre} | "
                f"{self.__duracion} h | {self.__estado.value} | costo: {costo}")
