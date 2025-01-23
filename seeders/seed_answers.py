from faker import Faker
from sqlalchemy.exc import IntegrityError
from app.models import Answer, Question
from extensions import db

fake = Faker('es_ES')

# Listado predefinido de respuestas asociadas a preguntas específicas
predefined_answers = {
    "¿Qué es la inteligencia artificial?": [
        {"text": "Un tipo de software", "is_correct": False},
        {"text": "Una simulación de procesos humanos por máquinas", "is_correct": True},
        {"text": "Un lenguaje de programación", "is_correct": False},
    ],
    "¿Cuáles son los planetas del sistema solar?": [
        {"text": "Mercurio, Venus, Tierra, Marte, Júpiter, Saturno, Urano y Neptuno", "is_correct": True},
        {"text": "Sol, Luna y Tierra", "is_correct": False},
    ],
    # Agrega más preguntas y respuestas según sea necesario...
}

def seed_answers():
    questions = Question.query.all()
    if not questions:
        print("No hay preguntas disponibles para asociar respuestas.")
        return

    for question in questions:
        try:
            # Verifica si hay respuestas predefinidas para la pregunta
            if question.text in predefined_answers:
                answers_data = predefined_answers[question.text]
                for answer_data in answers_data:
                    answer = Answer(
                        question_id=question.id,
                        text=answer_data["text"],
                        is_correct=answer_data["is_correct"],
                    )
                    db.session.add(answer)
                    db.session.commit()  # Guarda inmediatamente para manejar conflictos
            else:
                # Genera de 2 a 5 respuestas aleatorias si no hay predefinidas
                num_answers = fake.random_int(min=2, max=5)
                for i in range(num_answers):
                    answer = Answer(
                        question_id=question.id,
                        text=fake.sentence(nb_words=5),
                        is_correct=(i == 0),  # Marca la primera como correcta
                    )
                    db.session.add(answer)
                    db.session.commit()
        except IntegrityError:
            db.session.rollback()
            print(f"Respuestas duplicadas detectadas para la pregunta '{question.text}'. Saltando...")

    print("Respuestas creadas con éxito.")
