"""Clase abstracta que representa las entidades generales del sistema."""

import itertools                 # Para generar identificadores consecutivos
from abc import ABC, abstractmethod


class EntidadBase(ABC):
    """Entidad general: toda entidad tiene un identificador y se puede describir."""

    # Contador compartido que entrega 1, 2, 3, ... a cada entidad creada
    _contador = itertools.count(1)

    def __init__(self):
        # Atributo protegido: el identificador no debe modificarse desde fuera
        self._id = next(EntidadBase._contador)

    @property
    def id(self):
        """Identificador único de la entidad (solo lectura)."""
        return self._id

    @abstractmethod
    def describir(self):
        """Devuelve una descripción en texto; cada subclase debe implementarla."""

    def __str__(self):
        # Al imprimir cualquier entidad se usa su descripción
        return self.describir()
