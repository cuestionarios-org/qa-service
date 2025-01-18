from extensions import db
from .question import Question  # Relación con el modelo Question

class Answer(db.Model):
    __tablename__ = 'answers'
    
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)
    question = db.relationship('Question', backref=db.backref('answers', lazy=True))
    text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "is_correct": self.is_correct,
            "question_id": self.question_id,
        }
