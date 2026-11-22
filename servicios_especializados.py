"""Tres servicios especializados que heredan de Servicio (polimorfismo)."""

from numbers import Real

from excepciones import DatoInvalidoError, ParametroFaltanteError
from servicio import Servicio


class ReservaSala(Servicio):
    """Reserva de salas con capacidad máxima de personas."""

    def __init__(self, nombre, tarifa_hora, capacidad, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if isinstance(capacidad, bool) or not isinstance(capacidad, int) or capacidad <= 0:
            raise DatoInvalidoError(f"Capacidad inválida: {capacidad!r}.")
        self._capacidad = capacidad

    def calcular_costo(self, duracion_horas):
        """Tarifa por hora; 10 % de descuento por jornada completa (8 h o más)."""
        self._validar_duracion(duracion_horas)
        costo = self.tarifa_hora * duracion_horas
        return costo * 0.90 if duracion_horas >= 8 else costo

    def validar_parametros(self, **parametros):
        """Exige 'personas' y que no supere la capacidad de la sala."""
        if "personas" not in parametros:
            raise ParametroFaltanteError("La reserva de sala requiere el parámetro 'personas'.")
        personas = parametros["personas"]
        if isinstance(personas, bool) or not isinstance(personas, int) or personas <= 0:
            raise DatoInvalidoError(f"Número de personas inválido: {personas!r}.")
        if personas > self._capacidad:
            raise DatoInvalidoError(f"{personas} personas exceden la capacidad ({self._capacidad}).")

    def describir(self):
        return (f"Sala '{self.nombre}' | capacidad {self._capacidad} personas | "
                f"${self.tarifa_hora:,.0f}/h | {'disponible' if self.disponible else 'no disponible'}")


class AlquilerEquipo(Servicio):
    """Alquiler de equipos con cargo fijo de seguro."""

    def __init__(self, nombre, tarifa_hora, tipo_equipo, seguro, unidades, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if isinstance(seguro, bool) or not isinstance(seguro, Real) or seguro < 0:
            raise DatoInvalidoError(f"Seguro inválido: {seguro!r}.")
        if isinstance(unidades, bool) or not isinstance(unidades, int) or unidades <= 0:
            raise DatoInvalidoError(f"Unidades inválidas: {unidades!r}.")
        self._tipo_equipo = str(tipo_equipo)
        self._seguro = float(seguro)
        self._unidades = unidades

    def calcular_costo(self, duracion_horas):
        """Tarifa por hora más el seguro (cargo fijo)."""
        self._validar_duracion(duracion_horas)
        return self.tarifa_hora * duracion_horas + self._seguro

    def validar_parametros(self, **parametros):
        """Exige 'cantidad' y que no supere las unidades disponibles."""
        if "cantidad" not in parametros:
            raise ParametroFaltanteError("El alquiler de equipo requiere el parámetro 'cantidad'.")
        cantidad = parametros["cantidad"]
        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
            raise DatoInvalidoError(f"Cantidad inválida: {cantidad!r}.")
        if cantidad > self._unidades:
            raise DatoInvalidoError(f"Solo hay {self._unidades} unidades de '{self.nombre}'.")

    def describir(self):
        return (f"Equipo '{self.nombre}' ({self._tipo_equipo}) | {self._unidades} unidades | "
                f"${self.tarifa_hora:,.0f}/h + seguro ${self._seguro:,.0f}")


class AsesoriaEspecializada(Servicio):
    """Asesoría con recargo según el nivel del asesor."""

    # Factor multiplicador de la tarifa según el nivel
    NIVELES = {"junior": 1.0, "senior": 1.25, "experto": 1.5}
    MODALIDADES = ("virtual", "presencial")

    def __init__(self, nombre, tarifa_hora, especialidad, nivel, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if str(nivel).lower() not in self.NIVELES:
            raise DatoInvalidoError(f"Nivel inválido: {nivel!r}. Use {list(self.NIVELES)}.")
        self._especialidad = str(especialidad)
        self._nivel = str(nivel).lower()

    def calcular_costo(self, duracion_horas):
        """Tarifa por hora multiplicada por el factor del nivel del asesor."""
        self._validar_duracion(duracion_horas)
        return self.tarifa_hora * duracion_horas * self.NIVELES[self._nivel]

    def validar_parametros(self, **parametros):
        """Exige 'modalidad' virtual o presencial."""
        if "modalidad" not in parametros:
            raise ParametroFaltanteError("La asesoría requiere el parámetro 'modalidad'.")
        if parametros["modalidad"] not in self.MODALIDADES:
            raise DatoInvalidoError(f"Modalidad inválida: {parametros['modalidad']!r}.")

    def describir(self):
        return (f"Asesoría '{self.nombre}' | {self._especialidad} | nivel {self._nivel} | "
                f"${self.tarifa_hora:,.0f}/h")
