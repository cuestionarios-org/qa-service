# app/services/question_service.py
from app.models import Question
from extensions import db
from sqlalchemy.orm import joinedload

class QuestionService:

    @staticmethod
    def get_all_questions():
        """
        Obtiene todas las preguntas con sus respuestas y categorías relacionadas.
        """
        return (
            Question.query
            .options(joinedload(Question.answers), joinedload(Question.category))
            .all()
        )

    @staticmethod
    def get_question(id):
        return (Question.query
                .options(joinedload(Question.answers), joinedload(Question.category)).get_or_404(id)
                )
    
    
    @staticmethod
    def get_questions_by_category(category_id):
        return (Question.query
                .options(joinedload(Question.answers), joinedload(Question.category))
                .filter_by(category_id=category_id).all()
                )

    @staticmethod
    def create_question(data):
        question = Question(
        text=data['text'],
        category_id=data['category_id'],
        created_by=data['created_by'], 
        modified_by=data['created_by']
    )
        db.session.add(question)
        db.session.commit()
        return question

    @staticmethod
    def update_question(id, data):
        print(data)
        question = Question.query.get_or_404(id)
        print(question)
        question.text = data.get('text', question.text)
        question.modified_by = int(data.get('modified_by', question.modified_by))
        question.state = data.get('state', question.state)
        question.category_id = data.get('category_id', question.category_id)
        db.session.commit()
        return question

    @staticmethod
    def delete_question(id):
        question = Question.query.get_or_404(id)
        db.session.delete(question)
        db.session.commit()
