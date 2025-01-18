#!/bin/bash

# Espera a que PostgreSQL esté disponible
dockerize -wait tcp://postgres:5432 -timeout 30s

# Ejecuta las migraciones de la base de datos
flask db upgrade
echo "Base de datos disponible"

# Inicia la aplicación
python run.py
