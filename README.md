# Software FJ - Sistema Integral de Gestión de Clientes, Servicios y Reservas

Proyecto de la Fase 4 (componente práctico) del curso **Programación 213023** - UNAD.
Aplicación orientada a objetos en Python, **sin base de datos**: los datos viven en objetos y listas
internas, y los archivos solo se usan para el registro de eventos y errores.

## Ejecución

```bash
python main.py
```

Requiere Python 3.8 o superior y no usa librerías externas. El resultado de la simulación se guarda
en `logs/eventos.log`.

## Estructura

| Archivo | Contenido |
|---|---|
| `excepciones.py` | Excepciones personalizadas (`SoftwareFJError` y 6 derivadas) |
| `logger.py` | Registro de eventos y errores en `logs/eventos.log` |
| `entidad_base.py` | Clase abstracta `EntidadBase` |
| `cliente.py` | `Cliente` con encapsulación y validaciones |
| `servicio.py` | Clase abstracta `Servicio` y cálculo de costos con variantes |
| `servicios_especializados.py` | `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada` |
| `reserva.py` | `Reserva` (confirmar, cancelar, procesar) y `EstadoReserva` |
| `main.py` | Simulación de 23 operaciones válidas e inválidas |

## Conceptos aplicados

- **Abstracción:** `EntidadBase` y `Servicio` son clases abstractas (`ABC`).
- **Herencia y polimorfismo:** tres servicios sobrescriben `calcular_costo`, `describir` y `validar_parametros`.
- **Encapsulación:** datos del cliente y de la reserva en atributos privados con propiedades y validación.
- **Sobrecarga (parámetros opcionales):** `calcular_costo_total(horas)`, `(horas, impuesto)`, `(horas, impuesto, descuento)`.
- **Excepciones:** personalizadas, `try/except`, `try/except/else`, `try/except/finally` y encadenamiento con `raise ... from`.
- **Logs:** todo error y evento relevante queda registrado; el programa nunca se detiene ante un fallo.

## Autor

Eduar Gerardo Quitian Ruiz
