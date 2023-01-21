import os
from flask import Flask

#Creando la aplicacion, que estara conectada a una base de datos
def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY= 'mikey',  #Le asiganamos una cookie, para que no puedan modificar las sesione desde enlaces externos
        DATABASE_HOST = os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_PASSWORD = os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE_USER = os.environ.get('FLASK_DATABASE_USER'),
        DATABASE = os.environ.get('FLASK_DATABASE')
    )
 
    from . import db

    #llamamos la funcion de db init para cargar nuestra base a la app
    db.init_app(app)

    from . import auth
    from . import todo

    app.register_blueprint(auth.bp)
    app.register_blueprint(todo.bp)

    #creando una ruta de pruebas.
    @app.route('/hola')
    def hola():
        return 'Creando Proyecto'
    
    return app


 