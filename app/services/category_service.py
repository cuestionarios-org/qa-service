from app.models import Category
from extensions import db
from flask import jsonify

class CategoryService:
    
    @staticmethod
    def get_all_categories():
        categories = Category.query.all()
        return [category.to_dict() for category in categories]
    
    @staticmethod
    def get_category(id):
        category = Category.query.get_or_404(id)
        return category.to_dict()
    
    @staticmethod
    def create_category(data):
        category = Category(
            name=data['name'],
            description=data.get('description', '')
        )
        db.session.add(category)
        db.session.commit()
        return category.to_dict()
    
    @staticmethod
    def update_category(id, data):
        category = Category.query.get_or_404(id)
        category.name = data['name']
        category.description = data.get('description', category.description)
        db.session.commit()
        return category.to_dict()
    
    @staticmethod
    def delete_category(id):
        category = Category.query.get_or_404(id)
        db.session.delete(category)
        db.session.commit()
        return {'message': 'Category deleted successfully'}
