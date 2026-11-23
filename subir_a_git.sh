#!/usr/bin/env bash
# Ejecutar DENTRO del repositorio clonado, con los archivos del proyecto ya copiados.
# Uso: bash subir_a_git.sh
set -e

git pull origin main || true   # Trae lo que haya en el repositorio (ignora si está vacío)

commit() {  # commit "mensaje" archivo1 archivo2 ...
  local msg="$1"; shift
  git add "$@"
  git commit -m "$msg"
}

commit "chore: estructura inicial del proyecto y .gitignore" .gitignore
commit "feat: excepciones personalizadas del sistema" excepciones.py
commit "feat: clase abstracta EntidadBase y registro de logs" entidad_base.py logger.py
commit "feat: clase Cliente con validaciones y encapsulación" cliente.py
commit "feat: clase abstracta Servicio con cálculo de costos con variantes" servicio.py
commit "feat: servicios Sala, Equipo y Asesoría con polimorfismo" servicios_especializados.py
commit "feat: clase Reserva con confirmar, cancelar y procesar" reserva.py
commit "feat: simulación de 23 operaciones válidas e inválidas" main.py
commit "test: log de evidencia de la ejecución de la simulación" logs/eventos.log
commit "docs: README del proyecto" README.md

git push origin main
