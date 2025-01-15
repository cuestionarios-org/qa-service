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
