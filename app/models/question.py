from extensions import db
import datetime as dt
from app.utils.lib.pretty import pretty_print_dict
from .category import Category  # Relación con el modelo Category

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
        return {
            "id": self.id,
            "text": self.text,
            "category_id": self.category_id,
            "state": self.state,
            "created_by": self.created_by,
            "modified_by": self.modified_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        pretty_print_dict(self.to_dict())
        return ""
