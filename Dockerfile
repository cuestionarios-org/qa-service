FROM python:3.10

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de tu proyecto al contenedor
COPY . /app

# Instala las dependencias del proyecto
RUN pip install -r requirements.txt

# Espera a que PostgreSQL esté disponible
RUN apt-get update && apt-get install -y netcat
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Expón el puerto en el que el servicio de QA estará corriendo
EXPOSE 5003

# Ejecuta wait-for-it para esperar a PostgreSQL y luego iniciar la aplicación
CMD ["/wait-for-it.sh", "postgres:5432", "--", "python", "run.py"]
