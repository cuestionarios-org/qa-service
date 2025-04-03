# app/routes/quizzes.py

from flask import Blueprint, request, jsonify
from app.services import QuizService

quiz_bp = Blueprint('quiz', __name__)

# Ruta para crear un nuevo cuestionario

# Ruta para crear un cuestionario con preguntas
@quiz_bp.route('/', methods=['POST'])
def create_quiz():
    """
    Crea un cuestionario y asocia preguntas existentes mediante sus IDs.
    """
    data = request.get_json()

    if not data or 'quiz' not in data:
        return jsonify({"msg": "Invalid data. 'quiz' is required."}), 400

    quiz_data = data['quiz']
    question_ids = data.get('question_ids', None)  # IDs de preguntas opcionales

    try:
        quiz = QuizService.create_quiz_with_existing_questions(quiz_data, question_ids)
        return jsonify({"msg": "Quiz created successfully.", "quiz": quiz}), 201
    except ValueError as ve:
        return jsonify({"msg": str(ve)}), 400
    except Exception as e:
        return jsonify({"msg": "An error occurred.", "error": str(e)}), 500
    


# Ruta para obtener todos los cuestionarios
@quiz_bp.route('/', methods=['GET'])
def get_all_quizzes():
    """
    Lista todos los cuestionarios.
    """
    quizzes = QuizService.get_all_quizzes()
    result = []
    for quiz in quizzes:
        quiz_dict = quiz.to_dict()
        if 'questions' not in quiz_dict:
            quiz_dict['questions'] = []
        result.append(quiz_dict)
    return jsonify(result), 200

# Ruta para obtener un cuestionario por ID
@quiz_bp.route('/<int:id>', methods=['GET'])
def get_quiz_by_id(id):
    """
    Obtiene un cuestionario por ID.
    """
    quiz = QuizService.get_quiz(id)
    return jsonify(quiz.to_dict()), 200

# Ruta para obtener cuestionarios por categoría
@quiz_bp.route('/category/<int:category_id>', methods=['GET'])
def get_quizzes_by_category(category_id):
    """
    Lista los cuestionarios filtrados por categoría.
    """
    quizzes = QuizService.get_quizzes_by_category(category_id)
    result = [quiz.to_dict() for quiz in quizzes]
    return jsonify(result), 200

# Ruta para actualizar un cuestionario por ID
@quiz_bp.route('/<int:id>', methods=['PUT'])
def update_quiz(id):
    """
    Actualiza un cuestionario por ID, incluyendo su información y preguntas asociadas.
    """
    data = request.get_json()

    if not data or 'quiz' not in data:
        return jsonify({"msg": "Invalid data. 'quiz' is required."}), 400


    try:
        updated_quiz = QuizService.update_quiz(id, data)
        return jsonify({"msg": "Quiz updated successfully.", "quiz": updated_quiz}), 200
    except ValueError as ve:
        return jsonify({"msg": str(ve)}), 400
    except Exception as e:
        return jsonify({"msg": "An error occurred.", "error": str(e)}), 500

# Ruta para eliminar un cuestionario por ID
@quiz_bp.route('/<int:id>', methods=['DELETE'])
def delete_quiz(id):
    """
    Elimina un cuestionario por su ID.
    """
    try:
        QuizService.delete_quiz(id)
        return jsonify({"msg": "Quiz deleted successfully."}), 200
    except Exception as e:
        return jsonify({"msg": f"Error deleting quiz: {str(e)}"}), 400
