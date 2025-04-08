from flask import Blueprint, request, jsonify
from app.services.answer_service import AnswerService
from werkzeug.exceptions import BadRequest

answer_bp = Blueprint('answer', __name__)

@answer_bp.route('/answers/check', methods=['POST'])
def check_answers_bulk():
    """
    Endpoint para validar múltiples respuestas del usuario.
    """
    try:
        data = request.get_json()
        if not data or 'answers' not in data:
            raise BadRequest("Invalid data. 'answers' is required.")

        results = AnswerService.validate_bulk_answers(data['answers'])
        return jsonify({"answers": results}), 200

    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"❌ Error en /answers/check: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500
