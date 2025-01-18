# app/services/quiz_service.py
from app.models import Quiz, Question
from extensions import db
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError

class QuizService:

    @staticmethod
    def get_all_quizzes():
        """
        Obtiene todos los cuestionarios con sus preguntas y categorías relacionadas.
        """
        return (
            Quiz.query
            .options(joinedload(Quiz.questions), joinedload(Quiz.category))
            .all()
        )

    @staticmethod
    def get_quiz(id):
        """
        Obtiene un cuestionario por su id, incluyendo las preguntas y la categoría.
        """
        return (
            Quiz.query
            .options(joinedload(Quiz.questions), joinedload(Quiz.category))
            .get_or_404(id)
        )

    @staticmethod
    def get_quizzes_by_category(category_id):
        """
        Obtiene todos los cuestionarios por categoría.
        """
        return (
            Quiz.query
            .options(joinedload(Quiz.questions), joinedload(Quiz.category))
            .filter_by(category_id=category_id)
            .all()
        )

    @staticmethod
    def create_quiz(data):
        """
        Crea un nuevo cuestionario con las preguntas relacionadas.
        """
        quiz = Quiz(
            title=data['title'],
            description=data['description'],
            created_by=data['created_by'],
            modified_by=data['created_by'],
            category_id=data['category_id'],
            time_limit=data.get('time_limit', None),
            state=data.get('state', 'preparacion'),  # Estado predeterminado
            is_public=data.get('is_public', True),
            access_code=data.get('access_code', None),
            publish_at=data.get('publish_at', None)
        )
        
        try:
            db.session.add(quiz)
            db.session.commit()
            return quiz
        except IntegrityError:
            db.session.rollback()
            raise ValueError(f"El cuestionario con título '{data['title']}' ya existe en la categoría.")
    
    @staticmethod
    def create_quiz_with_existing_questions(quiz_data, question_ids=None):
        """
        Crea un cuestionario y asocia preguntas existentes mediante sus IDs.
        """
        try:
            # Crear el cuestionario
            quiz = Quiz(
                title=quiz_data['title'],
                description=quiz_data.get('description', None),
                created_by=quiz_data['created_by'],
                modified_by=quiz_data['created_by'],
                category_id=quiz_data['category_id'],
                time_limit=quiz_data.get('time_limit', None),
                state=quiz_data.get('state', 'preparacion'),
                is_public=quiz_data.get('is_public', True),
                access_code=quiz_data.get('access_code', None),
                publish_at=quiz_data.get('publish_at', None),
            )
            db.session.add(quiz)
            db.session.flush()  # Esto asegura que el `quiz.id` esté disponible antes de commit.

            # Validar y asociar preguntas existentes al cuestionario
            if question_ids:
                valid_question_ids = Question.query.filter(Question.id.in_(question_ids)).all()
                valid_question_ids = [q.id for q in valid_question_ids]  # Obtener IDs válidos

                if len(valid_question_ids) != len(question_ids):
                    invalid_ids = set(question_ids) - set(valid_question_ids)
                    raise ValueError(f"Los siguientes IDs de preguntas no son válidos: {invalid_ids}")

                for question_id in valid_question_ids:
                    QuizService.add_question_to_quiz(quiz.id, question_id)

            # Confirmar los cambios en la base de datos
            db.session.commit()

            return quiz.to_dict()

        except IntegrityError:
            db.session.rollback()
            raise ValueError(f"El cuestionario con título '{quiz_data['title']}' ya existe en la categoría.")
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al crear el cuestionario: {str(e)}")

    @staticmethod
    def update_quiz(id, data):
        """
        Actualiza un cuestionario y maneja la lista de preguntas asociadas.
        """
        quiz = Quiz.query.get_or_404(id)

        data_quiz = data.get('quiz', {})
        # Actualizar los atributos del cuestionario
        quiz.title = data_quiz.get('title', quiz.title)
        quiz.description = data_quiz.get('description', quiz.description)
        quiz.modified_by = data_quiz.get('modified_by', quiz.modified_by)
        quiz.category_id = data_quiz.get('category_id', quiz.category_id)
        quiz.time_limit = data_quiz.get('time_limit', quiz.time_limit)
        quiz.is_public = data_quiz.get('is_public', quiz.is_public)
        quiz.access_code = data_quiz.get('access_code', quiz.access_code)
        quiz.publish_at = data_quiz.get('publish_at', quiz.publish_at)

        # Cambiar el estado si se proporciona uno nuevo
        new_state = data_quiz.get('state')
        if new_state and new_state != quiz.state:
            try:
                quiz.set_state(new_state)
            except ValueError as e:
                raise ValueError(f"No se pudo actualizar el estado: {str(e)}")

        # Manejo de preguntas asociadas
        if 'question_ids' in data:
            new_question_ids = set(data['question_ids'])
            
            # Obtener las preguntas actuales asociadas al cuestionario
            current_question_ids = {q.id for q in quiz.questions}

            # Identificar preguntas a agregar y a eliminar
            to_add = new_question_ids - current_question_ids
            to_remove = current_question_ids - new_question_ids

            # Validar y agregar nuevas preguntas
            if to_add:
                valid_questions = Question.query.filter(Question.id.in_(to_add)).all()
                valid_question_ids = {q.id for q in valid_questions}
                if len(valid_question_ids) != len(to_add):
                    invalid_ids = to_add - valid_question_ids
                    raise ValueError(f"IDs de preguntas inválidos: {invalid_ids}")

                for question in valid_questions:
                    quiz.questions.append(question)

            # Eliminar preguntas que ya no están en la lista
            if to_remove:
                for question in quiz.questions:
                    if question.id in to_remove:
                        quiz.questions.remove(question)

        db.session.commit()
        return quiz.to_dict()

    @staticmethod
    def delete_quiz(id):
        """
        Elimina un cuestionario por su id.
        """
        quiz = Quiz.query.get_or_404(id)
        db.session.delete(quiz)
        db.session.commit()

    @staticmethod
    def change_quiz_state(id, new_state):
        """
        Cambia el estado de un cuestionario si la transición es válida.
        """
        quiz = Quiz.query.get_or_404(id)

        try:
            quiz.set_state(new_state)
            db.session.commit()
            return quiz
        except ValueError as e:
            # Si la transición no es válida, lanzamos una excepción con un mensaje adecuado
            db.session.rollback()
            raise ValueError(f"No se puede cambiar el estado: {str(e)}")


    @staticmethod
    def add_question_to_quiz(quiz_id, question_id):
        """
        Agrega una pregunta a un cuestionario si la transición es válida y la pregunta no está ya asociada.
        """
        try:
            # Obtener el cuestionario y la pregunta
            quiz = Quiz.query.get_or_404(quiz_id)
            question = Question.query.get_or_404(question_id)
            
            # Verificar el estado del cuestionario
            if quiz.state != 'preparacion':
                raise ValueError(f"No se puede agregar preguntas a un cuestionario en estado '{quiz.state}'. El estado debe ser 'preparcion'.")

            # Verificar si la pregunta ya está asociada al cuestionario
            if question in quiz.questions:
                raise ValueError(f"La pregunta '{question.text}' ya está asociada a este cuestionario.")
            
            # Agregar la pregunta al cuestionario
            quiz.questions.append(question)
            db.session.commit()

            return quiz
        
        except ValueError as e:
            # Si hay un error de validación, se puede manejar aquí
            db.session.rollback()  # Hacemos rollback en caso de error
            raise ValueError(f"Error al agregar la pregunta: {str(e)}")
        
        except Exception as e:
            # Capturamos cualquier otro tipo de excepción
            db.session.rollback()
            raise Exception(f"Ocurrió un error inesperado al agregar la pregunta: {str(e)}")


    @staticmethod
    def remove_question_from_quiz(quiz_id, question_id):
        """
        Elimina una pregunta de un cuestionario.
        """
        quiz = Quiz.query.get_or_404(quiz_id)
        question = Question.query.get_or_404(question_id)
        if question in quiz.questions:
            quiz.questions.remove(question)
            db.session.commit()
        return quiz
