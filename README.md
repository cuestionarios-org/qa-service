# 🧪 Servicio de Preguntas y Respuestas

Este proyecto implementa un sistema para gestionar preguntas y respuestas en cuestionarios utilizando Flask y PostgreSQL.

---

## 📂 **Estructura del Proyecto**
La estructura actual del proyecto sigue una organización clara y modular:
```
qa-service/
├── app/
│   ├── __init__.py         # Inicialización de la aplicación Flask
│   ├── config.py           # Configuración de Flask y PostgreSQL
│   ├── models.py           # Definición de modelos SQLAlchemy
│   ├── routes.py           # Definición de endpoints
│   ├── services/
│   │   ├── __init__.py     # Inicialización de servicios
│   │   ├── question_service.py  # Lógica del negocio para preguntas
│   │   └── response_service.py  # Lógica del negocio para respuestas
│   ├── repositories/
│   │   ├── __init__.py     # Inicialización de repositorios
│   │   ├── question_repository.py # Consultas a la base de datos para preguntas
│   │   └── response_repository.py # Consultas a la base de datos para respuestas
│   └── utils/
│       ├── __init__.py     # Inicialización de utilidades
│       ├── error_handlers.py # Manejo de errores personalizados
│       └── validators.py   # Validación de datos
├── migrations/
│   └── (archivos generados por Alembic)
├── tests/
│   ├── __init__.py         # Inicialización de pruebas
│   ├── test_routes.py      # Pruebas para los endpoints
│   ├── test_services.py    # Pruebas unitarias para servicios
│   └── test_models.py      # Pruebas unitarias para modelos
├── .env                    # Variables de entorno
├── .env.example            # Ejemplo de configuración de entorno
├── .flaskenv               # Configuración para Flask CLI
├── Dockerfile              # Dockerfile para crear la imagen
├── docker-compose.yml      # Configuración para entorno Docker
├── requirements.txt        # Dependencias de Python
└── README.md               # Documentación del servicio
```
---

## 🚀 Características

- CRUD para preguntas y respuestas.
- Asociación de preguntas a cuestionarios.
- Migraciones de base de datos con Alembic.
- Estructura escalable y modular.

## 📋 Requisitos

- Python 3.9+
- PostgreSQL
- pip (Python package installer)

## 🛠️ Instalación

1. Clona el repositorio:
    ```bash
    git clone https://github.com/fom78/qa-service.git
    cd qa-service
    ```

2. Crea un entorno virtual:
    ```bash
    python -m venv env
    ```

3. Activa el entorno virtual:
    - En Windows:
        ```bash
        .\env\Scripts\activate
        ```
    - En Unix o MacOS:
        ```bash
        source env/bin/activate
        ```

4. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Configuración

1. Configura las variables de entorno en un archivo `.env` en la raíz del proyecto:
    ```env
    FLASK_APP=app
    FLASK_ENV=development
    DATABASE_URL=postgresql://usuario:contraseña@localhost/qa_service
    ```

2. Asegurarse de tener la Base de datos corriendo.
    - para ellos puede ejecutar el contenedor.
    ```bash
    docker-compose up -d
    ```

3. Genera las migraciones de base de datos y aplícalas:
    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

## 🚀 Ejecución

Para iniciar la aplicación, ejecuta:
```bash
python run.py
```

El servicio estará disponible en `http://127.0.0.1:5003`.

## 🔄 Endpoints

### Categorías
- `POST /categories`: Crear una nueva Categoria.
```bash
{
  "name": "Geografía",
  "description": "Categoría para preguntas relacionadas con geografía."
}
```

### Preguntas
- `GET /questions`: Listar preguntas.
- `POST /questions`: Crear una nueva pregunta.
- `GET /questions/<id>`: Obtener detalles de una pregunta.
- `PUT /questions/<id>`: Actualizar una pregunta.
- `DELETE /questions/<id>`: Eliminar una pregunta.

### Respuestas
- `GET /responses`: Listar respuestas.
- `POST /responses`: Crear una nueva respuesta.
- `GET /responses/<id>`: Obtener detalles de una respuesta.
- `PUT /responses/<id>`: Actualizar una respuesta.
- `DELETE /responses/<id>`: Eliminar una respuesta.

## 🐳 Docker NO IMPLEMENTADO AUN

1. Construye la imagen de Docker:
    ```bash
    docker build -t qa-service .
    ```

2. Ejecuta el contenedor:
    ```bash
    docker-compose up
    ```

## 🖍️ Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.

---

Desarrollado con ❤️ por [Fernando Masino](https://github.com/fom78).

