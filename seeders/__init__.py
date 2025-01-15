from seeders.seed_categories import seed_categories
from seeders.seed_questions import seed_questions
from seeders.seed_answers import seed_answers

def run_seeders():
    print("Iniciando seeders...")
    seed_categories()
    seed_questions()
    seed_answers()
    print("Seeders completados con éxito.")
