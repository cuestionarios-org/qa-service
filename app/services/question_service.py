from app.models import Question
from extensions import db
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_
from flask import jsonify

class QuestionService:

    @staticmethod
    def get_all_questions(category_id=None, state=None):
        try:
            filters = []
            if category_id:
                filters.append(Question.category_id == category_id)
            if state:
                filters.append(Question.state == state)

            query = Question.query.options(
                joinedload(Question.answers),
                joinedload(Question.category)
            )
            if filters:
                query = query.filter(and_(*filters))

            return query.all()
        except SQLAlchemyError as e:
            print(f"❌ Error al obtener preguntas: {e}")
            return None
            

    @staticmethod
    def get_question(id):
        try:
            return (Question.query
                    .options(joinedload(Question.answers), joinedload(Question.category))
                    .get_or_404(id))
        except SQLAlchemyError as e:
            print(f"❌ Error al obtener la pregunta {id}: {e}")
            return None
    
    @staticmethod
    def get_questions_by_category(category_id):
        try:
            return (
                Question.query
                .options(joinedload(Question.answers), joinedload(Question.category))
                .filter_by(category_id=category_id)
                .all()
            )
        except SQLAlchemyError as e:
            print(f"❌ Error al obtener las preguntas para la categoria id: {category_id}: {e}")
            return None
        
    
    @staticmethod
    def create_question(data):
        try:
            question = Question(
                text=data['text'],
                category_id=data['category_id'],
                created_by=data['created_by'],
                modified_by=data['created_by']
            )
            db.session.add(question)
            db.session.commit()
            return question
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"❌ Error al crear pregunta: {e}")
            return None

    @staticmethod
    def update_question(id, data):
        try:
            question = Question.query.get_or_404(id)
            question.text = data.get('text', question.text)
            question.modified_by = int(data.get('modified_by', question.modified_by))
            question.state = data.get('state', question.state)
            question.category_id = data.get('category_id', question.category_id)
            db.session.commit()
            return question
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"❌ Error al actualizar pregunta {id}: {e}")
            return None

    @staticmethod
    def delete_question(id):
        try:
            question = Question.query.get_or_404(id)
            db.session.delete(question)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"❌ Error al eliminar pregunta {id}: {e}")
            return None
