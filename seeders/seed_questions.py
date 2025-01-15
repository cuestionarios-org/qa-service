from faker import Faker
from app.models import Question, Category
from extensions import db

fake = Faker('es_ES')

# Listado predefinido de preguntas con sus categorías asociadas
predefined_questions = [
    {"text": "¿Qué es la inteligencia artificial?", "category": "Tecnología", "difficulty": "medium"},
    {"text": "¿Cuáles son los planetas del sistema solar?", "category": "Ciencia", "difficulty": "easy"},
    {"text": "¿Quién ganó la última Copa del Mundo?", "category": "Deportes", "difficulty": "medium"},
    {"text": "¿Cuáles son los principales síntomas de la gripe?", "category": "Salud", "difficulty": "easy"},
    {"text": "¿Qué es el aprendizaje basado en proyectos?", "category": "Educación", "difficulty": "hard"},
    {"text": "¿Cuál es la película más taquillera de la historia?", "category": "Entretenimiento", "difficulty": "medium"},
    {"text": "¿Cuáles son los destinos turísticos más populares de 2023?", "category": "Viajes", "difficulty": "easy"},
    {"text": "¿Cómo se hace un pastel de chocolate?", "category": "Cocina", "difficulty": "easy"},
    {"text": "¿Cuáles son las tendencias de moda actuales?", "category": "Moda", "difficulty": "medium"},
    {"text": "¿Qué es la inflación y cómo afecta la economía?", "category": "Finanzas", "difficulty": "hard"},
]

def seed_questions():
    categories = Category.query.all()
    if not categories:
        print("No hay categorías disponibles para asociar preguntas.")
        return

    if predefined_questions:
        # Crear preguntas a partir del listado predefinido
        for question_data in predefined_questions:
            # Buscar la categoría correspondiente
            category = next((cat for cat in categories if cat.name == question_data["category"]), None)
            if category:
                question = Question(
                    text=question_data["text"],
                    category_id=category.id,
                    state="published",
                    created_by=fake.random_int(min=1, max=5),
                    modified_by=fake.random_int(min=1, max=5),
                    created_at=fake.date_time_this_year(),
                    updated_at=fake.date_time_this_year(),
                    meta_data={"difficulty": question_data["difficulty"]},
                )
                db.session.add(question)
    else:
        # Crear preguntas generadas automáticamente
        for _ in range(20):
            category = fake.random.choice(categories)
            question = Question(
                text=fake.sentence(nb_words=10),
                category_id=category.id,
                state=fake.random.choice(['draft', 'published']),
                created_by=fake.random_int(min=1, max=5),
                modified_by=fake.random_int(min=1, max=5),
                created_at=fake.date_time_this_year(),
                updated_at=fake.date_time_this_year(),
                meta_data={"difficulty": fake.random.choice(["easy", "medium", "hard"])},
            )
            db.session.add(question)

    db.session.commit()
    print("Preguntas creadas con éxito.")
