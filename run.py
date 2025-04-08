import os

from flask import Flask, jsonify
from app.config import config_dict
from extensions import db, migrate
from app.routes.categories import category_bp
from app.routes.questions import question_bp
from app.routes.quizzes import quiz_bp
from app.routes.answers import answer_bp
from sqlalchemy import text
from app.utils.commands.cli import seed, init_db
from app.utils.errors.handlers import register_error_handlers
from app.utils.db import create_database_if_not_exists

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
    app.register_blueprint(answer_bp, url_prefix='/answer')
    
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


if __name__ == '__main__':
    import os
    env = os.getenv('FLASK_ENV', 'development')
    PORT = os.getenv('QA_PORT', 5013)
    app = create_app(env)
    print(f"🚀 Aplicación Flask corriendo en http://localhost:{PORT} en modo {env}")
    app.run(host='0.0.0.0', port=PORT, debug=True)

