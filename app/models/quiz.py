from extensions import db
from sqlalchemy.orm import validates
import datetime as dt
from .category import Category
from .question import Question


class Quiz(db.Model):
    __tablename__ = 'quizzes'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    state = db.Column(db.String(50), nullable=False, default='preparacion')
    created_by = db.Column(db.Integer, nullable=False)
    modified_by = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=dt.datetime.now(dt.timezone.utc))
    updated_at = db.Column(db.DateTime, default=dt.datetime.now(dt.timezone.utc), onupdate=dt.datetime.now(dt.timezone.utc))
    time_limit = db.Column(db.Integer)  # Tiempo para responder las preguntas, en segundos
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='RESTRICT'), nullable=False)
    category = db.relationship('Category', backref=db.backref('quizzes', lazy=True))
    attempts = db.Column(db.Integer, default=0)  # Intentos totales
    is_public = db.Column(db.Boolean, default=True)
    access_code = db.Column(db.String(255), nullable=True)

    publish_at = db.Column(db.DateTime, nullable=True)

    __table_args__ = (
        db.UniqueConstraint('title', 'category_id', name='unique_quiz_title_per_category'),
    )

    # Relación muchos a muchos con Question a través de QuizQuestion
    questions = db.relationship('Question', 
                                 secondary='quiz_questions', 
                                 backref=db.backref('quizzes', lazy='dynamic'))
    # Validaciones
    @validates('time_limit')
    def validate_time_limit(self, key, value):
        if value is not None and value < 0:
            raise ValueError("El tiempo límite no puede ser negativo.")
        return value
    
    # Preferible a ENUM para evitar problemas en migraciones, por ahora
    @validates('state')
    def validate_state(self, key, value):
        allowed_states = ['preparacion', 'listo', 'inactivo', 'activo', 'finalizado']
        if value not in allowed_states:
            raise ValueError(f"El estado '{value}' no es válido.")
        return value
    
    def set_state(self, new_state):
        valid_transitions = {
            'preparacion': ['listo'],
            'listo': ['activo', 'inactivo'],
            'activo': ['finalizado', 'inactivo'],
            'inactivo': ['listo'],
        }
        if new_state not in valid_transitions.get(self.state, []):
            raise ValueError(f"No se puede cambiar de {self.state} a {new_state}.")
        self.state = new_state

    def __repr__(self):
        return f"<Quiz {self.title}>"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "state": self.state,
            "created_by": self.created_by,
            "modified_by": self.modified_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "time_limit": self.time_limit,
            "category_id": self.category_id,
            "questions": [q.to_dict() for q in self.questions],
        }
