from celery import Celery
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flask import Flask

def create_app(config_name):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///monitor.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    return app

app = create_app('default')
app_context = app.app_context()
app_context.push()

celery_app = Celery(__name__, broker='redis://localhost:6379/0')

db = SQLAlchemy()
db.init_app(app)
db.create_all()

class Entrenamiento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(50))
    distancia = db.Column(db.Float)
    tiempo = db.Column(db.Float)
    calorias = db.Column(db.Float)
    usuario_id = db.Column(db.Integer)

class EntrenamientoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Entrenamiento
        include_relationships = True
        load_instance = True

@celery_app.task(name='send_entrenamiento')
def send_entrenamiento(*args):
    with app.app_context():
        entrenamiento_schema = EntrenamientoSchema()
        entrenamiento = Entrenamiento(
            id=args[0],
            fecha=args[1],
            distancia=args[2],
            tiempo=args[3],
            calorias=args[4],
            usuario_id=args[5])
        db.session.add(entrenamiento)
        db.session.commit()
        print(entrenamiento)
        print([entrenamiento_schema.dumps(entreno) for entreno in Entrenamiento.query.all()])