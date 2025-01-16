#!/bin/bash
# wait-for-it.sh
# Espera hasta que el servicio de base de datos esté disponible

HOST=$1
PORT=$2
shift 2
CMD=$@

until nc -z -v -w30 $HOST $PORT; do
  echo "Esperando a PostgreSQL..."
  sleep 1
done

echo "PostgreSQL está listo."
exec $CMD
