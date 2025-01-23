from faker import Faker
from app.models import Category
from extensions import db
from sqlalchemy.exc import IntegrityError

fake = Faker('es_MX')

# Listado predefinido de categorías
predefined_categories = [
    {'name': 'Tecnología', 'description': 'Todo sobre avances tecnológicos'},
    {'name': 'Ciencia', 'description': 'Exploración científica y descubrimientos'},
    {'name': 'Deportes', 'description': 'Noticias y eventos deportivos'},
    {'name': 'Salud', 'description': 'Cuidado personal y bienestar'},
    {'name': 'Educación', 'description': 'Recursos educativos y aprendizaje'},
    {'name': 'Entretenimiento', 'description': 'Películas, series y música'},
    {'name': 'Viajes', 'description': 'Destinos y consejos para viajeros'},
    {'name': 'Cocina', 'description': 'Recetas y técnicas culinarias'},
    {'name': 'Moda', 'description': 'Tendencias y estilo personal'},
    {'name': 'Finanzas', 'description': 'Consejos para el manejo del dinero'},
]

def seed_categories():
    for category_data in predefined_categories:
        try:
            category = Category(
                name=category_data['name'],
                description=category_data['description'],
                created_at=fake.date_time_this_year(),
                updated_at=fake.date_time_this_year(),
            )
            db.session.add(category)
            db.session.commit()  # Intenta guardar inmediatamente para manejar conflictos
        except IntegrityError:
            db.session.rollback()  # Revierte cualquier cambio si hay un error
            print(f"Categoría '{category_data['name']}' ya existe. Saltando...")

    # Genera categorías aleatorias si no hay predefinidas
    if not predefined_categories:
        for _ in range(10):
            try:
                category = Category(
                    name=fake.unique.word().capitalize(),
                    description=fake.sentence(),
                    created_at=fake.date_time_this_year(),
                    updated_at=fake.date_time_this_year(),
                )
                db.session.add(category)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                print(f"Categoría generada aleatoriamente ya existe. Intentando otra...")

    print("Categorías creadas con éxito.")
