import os

from flask import Flask, jsonify
from app.config import config_dict
from extensions import db, migrate
from app.routes.categories import category_bp
from app.routes.questions import question_bp
from sqlalchemy import text

from seeders import run_seeders

from app.utils.errors.handlers import register_error_handlers


def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config_dict[config_name])
    
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(category_bp, url_prefix='/categories')
    app.register_blueprint(question_bp, url_prefix='/questions')
    
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
    
    # Registrar comandos personalizados
    @app.cli.command("seed")
    def seed():
        """Ejecuta todos los seeders."""
        print("Ejecutando seeders...")
        run_seeders()
        print("Seeders completados con éxito.")

    # Registra manejadores de errores
    
    register_error_handlers(app)
    
    return app

if __name__ == '__main__':
    import os
    env = os.getenv('FLASK_ENV', 'development')
    app = create_app(env)
    app.run(host='0.0.0.0', port=5003, debug=True)

