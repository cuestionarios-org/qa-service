from extensions import db
from datetime import datetime
import datetime as dt

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=dt.datetime.now(dt.timezone.utc))
    updated_at = db.Column(db.DateTime, default=dt.datetime.now(dt.timezone.utc), onupdate=dt.datetime.now(dt.timezone.utc))
    
    def __repr__(self):
        return f"<Category {self.name}>"
    
    # Método to_dict
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='RESTRICT'), nullable=False)
    category = db.relationship('Category', backref=db.backref('questions', lazy=True))
    state = db.Column(db.String(50), default='draft')
    created_by = db.Column(db.Integer, nullable=False)
    modified_by = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=dt.datetime.now(dt.timezone.utc))
    updated_at = db.Column(db.DateTime, default=dt.datetime.now(dt.timezone.utc), onupdate=dt.datetime.now(dt.timezone.utc))

    meta_data = db.Column(db.JSON)

    def to_dict(self):
        """
        Convierte el objeto Question en un diccionario serializable.
        """
        return {
            "id": self.id,
            "text": self.text,
            "category_id": self.category_id,
            "state": self.state,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

class Answer(db.Model):
    __tablename__ = 'answers'
    
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)
    question = db.relationship('Question', backref=db.backref('answers', lazy=True))
    text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)

    def to_dict(self):
        """
        Convierte el objeto Answer en un diccionario serializable.
        """
        return {
            "id": self.id,
            "text": self.text,
            "is_correct": self.is_correct,
            "question_id": self.question_id,
        }
