#!/bin/bash

echo "<<<<<<<<< ${QA_POSTGRES_HOST} >>>>>>>>>"


# Verifica que las variables necesarias estén configuradas
if [[ -z "$QA_POSTGRES_HOST" || -z "$QA_POSTGRES_PORT" || -z "$QA_POSTGRES_DB" ]]; then
    echo "Error: Las variables POSTGRES_HOST, POSTGRES_PORT o POSTGRES_DB no están configuradas."
    exit 1
fi


# Espera a que PostgreSQL esté disponible
dockerize -wait tcp://$QA_POSTGRES_HOST:$QA_POSTGRES_PORT -timeout 30s
if [ $? -ne 0 ]; then
    echo "Error: No se pudo conectar a PostgreSQL en $QA_POSTGRES_HOST:$QA_POSTGRES_PORT"
    exit 1
fi


# Inicia la aplicación
python run.py
