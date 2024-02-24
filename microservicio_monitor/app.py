# from .modelos import db, Entrenamiento, EntrenamientoSchema
from datetime import datetime
from flask import request
from flask_restful import Api,Resource
from .tarea import create_app, db, Entrenamiento, EntrenamientoSchema, app
from celery import Celery

entrenamiento_schema = EntrenamientoSchema()

class EntrenamientoResourceQ(Resource):
    def get(self):
        entrenamientos = Entrenamiento.query.all()
        return entrenamiento_schema.dump(entrenamientos, many=True)
    
api = Api(app)

api.add_resource(EntrenamientoResourceQ, '/entrenamientos')