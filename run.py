import os

from flask import Flask, jsonify
from app.config import config_dict
from extensions import db, migrate
from app.routes.categories import category_bp
from app.routes.questions import question_bp
from app.routes.quizzes import quiz_bp
from sqlalchemy import text, create_engine
from app.utils.commands.cli import seed, init_db
from flask_migrate import upgrade
from seeders import run_seeders

from app.utils.errors.handlers import register_error_handlers


def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config_dict[config_name])

    
    db.init_app(app)
    migrate.init_app(app, db)

    # Intentar crear la base de datos si no existe
    create_database_if_not_exists(app)

    app.cli.add_command(init_db)
    app.cli.add_command(seed)

    app.register_blueprint(category_bp, url_prefix='/categories')
    app.register_blueprint(question_bp, url_prefix='/questions')
    app.register_blueprint(quiz_bp, url_prefix='/quizzes')
    
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Welcome to the Flask application!',
            'status': 'success',
            'documentation': '/docs'  # Ejemplo de ruta de documentación
        })
    
    @app.route('/health/db', methods=['GET'])
    def check_db_connection():
        try:
            # Usa text() para declarar la consulta
            db.session.execute(text('SELECT 1'))
            return jsonify({'status': 'ok', 'message': 'Database connection successful'}), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    
    register_error_handlers(app)

    return app

def create_database_if_not_exists(app):
    """Crea la base de datos en PostgreSQL si no existe"""
    print("😝 exite db ?")
    db_url = app.config["SQLALCHEMY_DATABASE_URI"]
    
    # Conectar a la base `postgres` en lugar de la que aún no existe
    temp_db_url = db_url.rsplit("/", 1)[0] + "/postgres"
    engine = create_engine(temp_db_url, isolation_level="AUTOCOMMIT")  # 🔥 Se agrega `isolation_level="AUTOCOMMIT"`

    with engine.connect() as connection:
        db_name = os.getenv('QA_POSTGRES_DB')
        result = connection.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'"))
        exists = result.scalar()
        
        if not exists:
            print(f"📌 Creando la base de datos {db_name}...")
            connection.execute(text(f"CREATE DATABASE {db_name}"))
            print(f"✅ Base de datos {db_name} creada exitosamente.")

            # 🔥 Ejecutar migraciones usando Flask Migrate directamente
            print("📌 Ejecutando migraciones...")
            with app.app_context():
                try:
                    upgrade()
                    print("✅ Migraciones aplicadas correctamente.")
                    # Insertar usuarios con cada rol
                    print("📌 Iniciando seeders...")
                    run_seeders()
                    print("✅ Rutina de seeders finalizada.")
                except Exception as e:
                    print(f"❌ Error al aplicar migraciones: {e}")
        else:
            print(f"✅ La base de datos {db_name} ya existe.")

if __name__ == '__main__':
    import os
    env = os.getenv('FLASK_ENV', 'development')
    PORT = os.getenv('QA_PORT', 5013)
    app = create_app(env)
    print(f"🚀 Aplicación Flask corriendo en http://localhost:{PORT} en modo {env}")
    app.run(host='0.0.0.0', port=PORT, debug=True)

