"""Clase abstracta Servicio y cálculo de costos con variantes (sobrecarga)."""

from abc import ABC, abstractmethod
from numbers import Real

from entidad_base import EntidadBase
from excepciones import (CalculoInconsistenteError, DatoInvalidoError,
                         ParametroFaltanteError)


class Servicio(EntidadBase, ABC):
    """Servicio general ofrecido por Software FJ."""

    IVA_POR_DEFECTO = 0.19  # 19 % de IVA en Colombia

    def __init__(self, nombre, tarifa_hora, disponible=True):
        super().__init__()
        # Validación del nombre
        if nombre is None or str(nombre).strip() == "":
            raise ParametroFaltanteError("El nombre del servicio es obligatorio.")
        # Validación de la tarifa: número real positivo (bool no cuenta como número)
        if isinstance(tarifa_hora, bool) or not isinstance(tarifa_hora, Real) or tarifa_hora <= 0:
            raise DatoInvalidoError(f"Tarifa por hora inválida: {tarifa_hora!r}.")
        self._nombre = str(nombre).strip()
        self._tarifa_hora = float(tarifa_hora)
        self._disponible = bool(disponible)

    # ---- propiedades de solo lectura / lectura-escritura ----
    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_hora(self):
        return self._tarifa_hora

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, valor):
        self._disponible = bool(valor)

    # ---- métodos abstractos (polimorfismo) ----
    @abstractmethod
    def calcular_costo(self, duracion_horas):
        """Costo base sin impuestos ni descuentos; cada servicio lo sobrescribe."""

    @abstractmethod
    def validar_parametros(self, **parametros):
        """Valida los parámetros propios de cada servicio al reservar."""

    # ---- validación de duración reutilizable ----
    @staticmethod
    def _validar_duracion(duracion_horas):
        if isinstance(duracion_horas, bool) or not isinstance(duracion_horas, Real) or duracion_horas <= 0:
            raise DatoInvalidoError(f"Duración inválida: {duracion_horas!r}.")

    # ---- método con variantes (sobrecarga simulada con parámetros opcionales) ----
    def calcular_costo_total(self, duracion_horas, impuesto=None, descuento=None):
        """Calcula el costo final. Variantes de llamada:

        - calcular_costo_total(h)                 -> costo base + IVA por defecto
        - calcular_costo_total(h, 0.05)           -> costo base + impuesto indicado
        - calcular_costo_total(h, 0.19, 0.10)     -> con impuesto y descuento
        - calcular_costo_total(h, descuento=0.10) -> IVA por defecto y descuento
        """
        # Si no se indica impuesto se usa el IVA; si no se indica descuento es 0
        impuesto = self.IVA_POR_DEFECTO if impuesto is None else impuesto
        descuento = 0.0 if descuento is None else descuento
        # Validación de rangos: impuesto en [0, 1) y descuento en [0, 1]
        if not 0 <= impuesto < 1:
            raise CalculoInconsistenteError(f"Impuesto fuera de rango: {impuesto}.")
        if not 0 <= descuento <= 1:
            raise CalculoInconsistenteError(f"Descuento fuera de rango: {descuento}.")
        base = self.calcular_costo(duracion_horas)           # polimorfismo
        total = base * (1 - descuento) * (1 + impuesto)
        # Un total negativo o nulo indicaría un cálculo inconsistente
        if total <= 0:
            raise CalculoInconsistenteError(f"Costo total inconsistente: {total}.")
        return round(total, 2)
