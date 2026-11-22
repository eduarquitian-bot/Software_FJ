"""Clase Cliente con encapsulación y validaciones estrictas."""

import re  # Expresiones regulares para validar el correo

from entidad_base import EntidadBase
from excepciones import DatoInvalidoError, ParametroFaltanteError


class Cliente(EntidadBase):
    """Cliente de Software FJ. Sus datos personales son privados."""

    # Patrón sencillo de correo: texto@dominio.ext
    _PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")

    def __init__(self, nombre, documento, correo, telefono):
        super().__init__()
        # Cada asignación pasa por el setter, que valida el dato
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

    # ---- utilidades de validación ----
    @staticmethod
    def _requerido(valor, campo):
        """Verifica que el parámetro exista y no esté vacío."""
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError(f"El campo '{campo}' es obligatorio.")
        return str(valor).strip()

    # ---- nombre ----
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        valor = self._requerido(valor, "nombre")
        # Solo letras y espacios (se permiten tildes y ñ), mínimo 3 caracteres
        if len(valor) < 3 or not all(c.isalpha() or c.isspace() for c in valor):
            raise DatoInvalidoError(f"Nombre inválido: '{valor}'.")
        self.__nombre = valor.title()

    # ---- documento ----
    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        valor = self._requerido(valor, "documento")
        # Solo dígitos, entre 5 y 12
        if not valor.isdigit() or not 5 <= len(valor) <= 12:
            raise DatoInvalidoError(f"Documento inválido: '{valor}' (5 a 12 dígitos).")
        self.__documento = valor

    # ---- correo ----
    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        valor = self._requerido(valor, "correo")
        if not self._PATRON_CORREO.match(valor):
            raise DatoInvalidoError(f"Correo inválido: '{valor}'.")
        self.__correo = valor.lower()

    # ---- teléfono ----
    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        valor = self._requerido(valor, "teléfono")
        if not valor.isdigit() or not 7 <= len(valor) <= 10:
            raise DatoInvalidoError(f"Teléfono inválido: '{valor}' (7 a 10 dígitos).")
        self.__telefono = valor

    def describir(self):
        """Descripción del cliente (implementa el método abstracto)."""
        return f"Cliente #{self.id}: {self.nombre} | Doc: {self.documento} | {self.correo} | Tel: {self.telefono}"
