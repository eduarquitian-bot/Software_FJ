"""Punto de entrada: simulación de operaciones del sistema Software FJ."""

from cliente import Cliente
from excepciones import (OperacionNoPermitidaError, SoftwareFJError)
from logger import RUTA_LOG, configurar_logger, registrar_error, registrar_evento
from reserva import Reserva
from servicios_especializados import (AlquilerEquipo, AsesoriaEspecializada,
                                      ReservaSala)


class GestorFJ:
    """Administra las listas internas de clientes, servicios y reservas (sin base de datos)."""

    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, nombre, documento, correo, telefono):
        cliente = Cliente(nombre, documento, correo, telefono)
        # No se permiten dos clientes con el mismo documento
        if any(c.documento == cliente.documento for c in self.clientes):
            raise OperacionNoPermitidaError(f"Ya existe un cliente con documento {cliente.documento}.")
        self.clientes.append(cliente)
        registrar_evento(f"Cliente registrado: {cliente.describir()}")
        return cliente

    def agregar_servicio(self, servicio):
        self.servicios.append(servicio)
        registrar_evento(f"Servicio creado: {servicio.describir()}")
        return servicio

    def crear_reserva(self, cliente, servicio, horas, **parametros):
        reserva = Reserva(cliente, servicio, horas, **parametros)
        self.reservas.append(reserva)
        registrar_evento(f"Reserva creada: {reserva.describir()}")
        return reserva


def ejecutar(numero, descripcion, accion):
    """Ejecuta una operación de la simulación sin que un error detenga el programa."""
    print(f"\n[{numero:02d}] {descripcion}")
    try:
        resultado = accion()
    except SoftwareFJError as error:
        # Error controlado propio del sistema
        print(f"     ✗ Error controlado: {error}")
        if error.__cause__:
            print(f"       causa original: {type(error.__cause__).__name__}: {error.__cause__}")
        registrar_error(f"Operación {numero:02d} ({descripcion}) falló: {error}", error)
        return None
    except Exception as error:  # Red de seguridad para errores inesperados
        print(f"     ✗ Error inesperado: {type(error).__name__}: {error}")
        registrar_error(f"Operación {numero:02d} ({descripcion}) error inesperado: {type(error).__name__}: {error}")
        return None
    else:
        print(f"     ✓ OK: {resultado}")
        registrar_evento(f"Operación {numero:02d} ({descripcion}) exitosa.")
        return resultado
    finally:
        # Se ejecuta siempre: deja constancia de que la operación terminó
        registrar_evento(f"Operación {numero:02d} finalizada.")


def simular():
    """Simula 18 operaciones válidas e inválidas."""
    configurar_logger("w")  # Se reinicia el log para dejar evidencia limpia
    registrar_evento("=== Inicio de la simulación de Software FJ ===")
    g = GestorFJ()

    # ---------- Clientes ----------
    ana = ejecutar(1, "Registrar cliente válido (Ana)",
                   lambda: g.registrar_cliente("ana maría pérez", "1020304050", "ana@correo.com", "3001234567"))
    carlos = ejecutar(2, "Registrar cliente válido (Carlos)",
                      lambda: g.registrar_cliente("Carlos Ruiz", "79854123", "carlos.ruiz@mail.co", "3109876543"))
    ejecutar(3, "Registrar cliente con correo inválido",
             lambda: g.registrar_cliente("Luis Gómez", "12345678", "luis-sin-arroba", "3001112233"))
    ejecutar(4, "Registrar cliente sin documento (parámetro faltante)",
             lambda: g.registrar_cliente("Marta Díaz", None, "marta@correo.com", "3004445566"))
    ejecutar(5, "Registrar cliente con documento duplicado",
             lambda: g.registrar_cliente("Ana Duplicada", "1020304050", "otra@correo.com", "3007778899"))

    # ---------- Servicios ----------
    sala = ejecutar(6, "Crear servicio de sala válido",
                    lambda: g.agregar_servicio(ReservaSala("Sala Innovación", 50000, 12)))
    equipo = ejecutar(7, "Crear servicio de alquiler de equipo válido",
                      lambda: g.agregar_servicio(AlquilerEquipo("Portátil Pro", 15000, "Portátil", 20000, 5)))
    asesoria = ejecutar(8, "Crear servicio de asesoría válido",
                        lambda: g.agregar_servicio(AsesoriaEspecializada("Asesoría Cloud", 80000, "Cloud", "senior")))
    ejecutar(9, "Crear servicio con tarifa negativa",
             lambda: g.agregar_servicio(ReservaSala("Sala Falsa", -100, 5)))
    cerrada = ejecutar(10, "Crear sala no disponible (mantenimiento)",
                       lambda: g.agregar_servicio(ReservaSala("Sala Mantenimiento", 40000, 8, disponible=False)))

    # ---------- Reservas ----------
    r1 = ejecutar(11, "Reserva válida de sala (10 personas, 3 h)",
                  lambda: g.crear_reserva(ana, sala, 3, personas=10))
    ejecutar(12, "Confirmar y procesar con IVA 19 % y 10 % de descuento",
             lambda: (r1.confirmar(), r1.procesar(0.19, 0.10))[1])
    ejecutar(13, "Reserva de sala que excede la capacidad (encadenamiento)",
             lambda: g.crear_reserva(carlos, sala, 2, personas=30))
    ejecutar(14, "Reserva con duración no numérica (encadenamiento)",
             lambda: g.crear_reserva(carlos, equipo, "abc", cantidad=1))
    ejecutar(15, "Reserva de un servicio no disponible",
             lambda: g.crear_reserva(ana, cerrada, 2, personas=3))
    ejecutar(16, "Reserva de asesoría sin el parámetro 'modalidad'",
             lambda: g.crear_reserva(ana, asesoria, 2))
    r2 = ejecutar(17, "Reserva válida de equipo y cancelación",
                  lambda: g.crear_reserva(carlos, equipo, 5, cantidad=2))
    ejecutar(18, "Cancelar la reserva de equipo", lambda: r2.cancelar())
    ejecutar(19, "Procesar una reserva cancelada (operación no permitida)", lambda: r2.procesar())
    r3 = ejecutar(20, "Reserva válida de asesoría virtual",
                  lambda: g.crear_reserva(carlos, asesoria, 2, modalidad="virtual"))
    ejecutar(21, "Procesar una reserva sin confirmar", lambda: r3.procesar())
    ejecutar(22, "Confirmar y procesar con descuento fuera de rango (cálculo inconsistente)",
             lambda: (r3.confirmar(), r3.procesar(descuento=1.5))[1])
    ejecutar(23, "Procesar de nuevo con variante por defecto (solo IVA)", lambda: r3.procesar())

    # ---------- Resumen ----------
    registrar_evento("=== Fin de la simulación: el sistema continuó estable ===")
    print("\n" + "=" * 60)
    print(f"Clientes: {len(g.clientes)} | Servicios: {len(g.servicios)} | Reservas: {len(g.reservas)}")
    for r in g.reservas:
        print("  ", r.describir())
    print(f"Log de eventos y errores: {RUTA_LOG}")


if __name__ == "__main__":
    simular()
