import mysql.connector
import click
from flask import current_app, g
from flask.cli import with_appcontext
from .schema import instructions


#Conectamos la base de datos q la app que se encuentra en init
def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=current_app.config['DATABASE_HOST'],
            user=current_app.config['DATABASE_USER'],
            password=current_app.config['DATABASE_PASSWORD'],
            database=current_app.config['DATABASE']
        )

        g.c = g.db.cursor(dictionary = True)
    return g.db, g.c 


# Dejamos que Flask se ocupe de cerrar la base de datos automaticamente luego de usarla.
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db, c = get_db()
    
    for i in instructions:
        c.execute(i)

    db.commit()

#usar la terminar para inicializar la db con comandos
@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Base de Datos inicializada')

#Esta Funcion le dira a flask que la base de datos debe cerrarse luego de cada peticion.
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

