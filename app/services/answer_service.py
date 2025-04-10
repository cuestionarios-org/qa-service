# app/services/answer_service.py

from app.models import Answer
from extensions import db
from werkzeug.exceptions import BadRequest

class AnswerService:
    @staticmethod
    def create_answers(data, question_id):
        """
        Crea múltiples respuestas asociadas a una pregunta en una sola operación.
        :param data: Lista de diccionarios con los datos de cada respuesta.
        :param question_id: ID de la pregunta asociada.
        :return: Lista de instancias de respuestas creadas.
        """
        if not data or not isinstance(data, list):
            raise BadRequest("Invalid data. 'answers' must be a list of answer objects.")

        answers = []
        for answer_data in data:
            if 'text' not in answer_data or 'is_correct' not in answer_data:
                raise BadRequest("Each answer must include 'text' and 'is_correct'.")

            answers.append(Answer(
                text=answer_data['text'],
                is_correct=answer_data['is_correct'],
                question_id=question_id
            ))

        # Agregar todas las respuestas en una sola operación
        # No retorna el id de las respuestas pero no sera necesario en este punto
        db.session.bulk_save_objects(answers)
        # db.session.add_all(answers)
        db.session.commit()
        # db.session.refresh(answers)  # Sincroniza los IDs generados
        return answers
    
    @staticmethod
    def delete_answers_by_question_id(question_id):
        """
        Elimina todas las respuestas asociadas a una pregunta específica.
        :param question_id: ID de la pregunta cuyas respuestas deben ser eliminadas.
        """
        if not question_id:
            raise ValueError("A valid 'question_id' is required.")

        try:
            # Eliminar todas las respuestas asociadas al question_id
            db.session.query(Answer).filter_by(question_id=question_id).delete()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise RuntimeError(f"Error while deleting answers for question_id {question_id}: {e}")


    @staticmethod
    def validate_bulk_answers(answers_input):
        """
        Valida múltiples respuestas y devuelve una lista con los IDs de la respuesta correcta
        para cada pregunta junto con la respuesta enviada por el usuario.
        """
        if not answers_input or not isinstance(answers_input, list):
            raise BadRequest("'answers' must be a non-empty list of answer objects.")

        results = []

        for item in answers_input:
            question_id = item.get("question_id")
            user_answer_id = item.get("answer_id")

            if not question_id or not user_answer_id:
                continue  # O podrías acumular errores y reportarlos

            correct_answer = Answer.query.filter_by(
                question_id=question_id, is_correct=True
            ).first()

            if not correct_answer:
                continue  # No se encontró respuesta correcta para la pregunta

            results.append({
                "question_id": question_id,
                "answer_id": user_answer_id,
                "correct_answer_id": correct_answer.id
            })

        return results