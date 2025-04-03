from flask import jsonify
from app.utils.errors.CustomException import CustomException
from app.utils.logs.logger_config import setup_logging
import logging
from sqlalchemy.exc import OperationalError

# Configurar logging al iniciar la aplicación
setup_logging()

def register_error_handlers(app):
    """
    Registra manejadores de errores personalizados en la aplicación Flask.
    """
    @app.errorhandler(CustomException)
    def handle_custom_exception(error):
        """
        Maneja excepciones personalizadas y devuelve una respuesta JSON.
        """
        response = jsonify(error.to_dict())
        response.status_code = error.code
        return response

# Middleware para capturar errores globales
    @app.errorhandler(OperationalError)
    def handle_db_connection_error(e):
        print(f"🔴 Error de conexión a la base de datos: {e}")
        return jsonify({
            "error": "No se pudo conectar a la base de datos",
            "details": "Asegúrate de que el servidor PostgreSQL esté corriendo."
        }), 500

    @app.errorhandler(404)
    def handle_404(error):
        """
        Maneja errores 404 (no encontrado).
        """
        return jsonify({"msg": "Recurso no encontrado", "error": "404", "details": str(error)}), 404
    

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        """
        Maneja cualquier excepción no controlada.
        """
        logger = logging.getLogger(__name__)
        logger.error(f"Unhandled Exception: {str(error)}", exc_info=True)
        response = jsonify({
            "error": "An unexpected error occurred",
            "details": str(error),
            "code": 500
        })
        response.status_code = 500
        return response
