# app/routes/question_answers.py

from flask import Blueprint, request, jsonify
from app.services import QuestionService
from app.services import AnswerService
from sqlalchemy.exc import SQLAlchemyError

question_bp = Blueprint('question', __name__)

# Ruta para crear una pregunta con respuestas
@question_bp.route('/', methods=['POST'])
def create_question_with_answers():
    """
    Crea una pregunta con sus respuestas asociadas.
    """
    data = request.get_json()

    if not data or 'question' not in data or 'answers' not in data:
        return jsonify({"msg": "Invalid data. 'question' and 'answers' are required."}), 400

    question_data = data['question']
    answers_data = data['answers']

    # Crear la pregunta
    question = QuestionService.create_question(question_data)

    # Crear las respuestas asociadas a la pregunta
    answers = AnswerService.create_answers(answers_data, question.id)

    return jsonify({
        'question': question.to_dict(),
        'answers': [answer.to_dict() for answer in answers]
    }), 201

# Ruta para listar todas las preguntas con sus respuestas
@question_bp.route('/', methods=['GET'])
def get_all_questions_with_answers():
    try:
        category_id = request.args.get('category_id', type=int)
        state = request.args.get('state', type=str)

        questions = QuestionService.get_all_questions(category_id, state)

        if questions is None:
            return jsonify({"error": "Error al obtener preguntas"}), 500

        result = [
            {
                'question': question.to_dict(),
                'answers': [answer.to_dict() for answer in question.answers]
            }
            for question in questions
        ]
        return jsonify(result), 200
    except SQLAlchemyError as e:
        print(f"❌ Error en la ruta /questions: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500
        
# Ruta para obtener una pregunta por ID con sus respuestas
@question_bp.route('/<int:id>', methods=['GET'])
def get_question_by_id(id):
    try:
        question = QuestionService.get_question(id)
        if question is None:
            return jsonify({"error": "Pregunta no encontrada"}), 404

        return jsonify({
            'question': question.to_dict(),
            'answers': [answer.to_dict() for answer in question.answers]
        }), 200
    except SQLAlchemyError as e:
        print(f"❌ Error en la ruta /questions/{id}: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

# Ruta para filtrar preguntas por categoría
@question_bp.route('/category/<int:category_id>', methods=['GET'])
def get_questions_by_category(category_id):
    """
    Lista preguntas filtradas por categoría.
    """
    questions = QuestionService.get_questions_by_category(category_id)

    
    result = [
        {
            'question': question.to_dict(),
            'answers': [answer.to_dict() for answer in question.answers]
        }
        for question in questions
    ]
    
    return jsonify(result), 200

# Ruta para actualizar una pregunta con sus respuestas
@question_bp.route('/<int:id>', methods=['PUT'])
def update_question_with_answers(id):
    """
    Actualiza una pregunta y sus respuestas asociadas.
    """
    data = request.get_json()

    if not data or 'question' not in data or 'answers' not in data:
        return jsonify({"msg": "Invalid data. 'question' and 'answers' are required."}), 400

    question_data = data['question']
    answers_data = data['answers']

    # Actualizar la pregunta
    question = QuestionService.update_question(id, question_data)

    # Eliminar respuestas existentes y crear nuevas
    AnswerService.delete_answers_by_question_id(id)
    answers = AnswerService.create_answers(answers_data, question.id)

    return jsonify({
        'question': question.to_dict(),
        'answers': [answer.to_dict() for answer in answers]
    }), 200
