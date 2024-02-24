from microservicio_objetivos import create_app
from flask_restful import Api, Resource
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from .modelos import Entrenamiento, EntrenamientoSchema,db
from datetime import datetime
from microservicio_objetivos.api_commands import EntrenamientoResourceC
from microservicio_objetivos.api_queries import EntrenamientoResourceQ

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)

api.add_resource(EntrenamientoResourceC, '/api-commands/entrenamientos')
api.add_resource(EntrenamientoResourceQ, '/api-queries/entrenamientos')

with app.app_context():
    entrenamiento = Entrenamiento(fecha=datetime.now(), distancia=10, tiempo=60, calorias=500, usuario_id=1)
    db.session.add(entrenamiento)
    db.session.commit()