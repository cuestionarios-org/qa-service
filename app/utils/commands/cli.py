
from flask import current_app
from flask.cli import with_appcontext
import click
from psycopg2 import connect
from seeders import run_seeders

@click.command("init_db")
@with_appcontext
def init_db():
    """Verifica y crea la base de datos si no existe."""
    from sqlalchemy.engine.url import make_url
    db_url = make_url(current_app.config['SQLALCHEMY_DATABASE_URI'])
    db_name = db_url.database

    default_db_url = db_url.set(database='postgres')
    try:
        conn = connect(
            dbname=default_db_url.database,
            user=default_db_url.username,
            password=default_db_url.password,
            host=default_db_url.host,
            port=default_db_url.port,
        )
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
            if not cursor.fetchone():
                cursor.execute(f"CREATE DATABASE {db_name}")
                click.echo(f"Base de datos '{db_name}' creada exitosamente.")
            else:
                click.echo(f"La base de datos '{db_name}' ya existe.")
            if current_app.config['SEED_DB'] == 'si':
                run_seeders()

    except Exception as e:
        click.echo(f"Error al verificar/crear la base de datos '{db_name}': {e}")
    finally:
        conn.close()


@click.command("seed")
@with_appcontext
def seed():
    """Ejecuta todos los seeders."""
    click.echo("Ejecutando seeders...")
    run_seeders()
    click.echo("Seeders completados con éxito.")