from microservicio_objetivos.app import db, Entrenamiento, EntrenamientoSchema, Resource, request, datetime
from celery import Celery

celery_app = Celery(__name__, broker='redis://localhost:6379/0')

@celery_app.task(name='send_entrenamiento')
def send_entrenamiento(*args):
    pass

entrenamiento_schema = EntrenamientoSchema()

class EntrenamientoResourceC(Resource):
    def post(self):
        new_entrenamiento = Entrenamiento(
            fecha=datetime.strptime(request.json['fecha'], '%y-%m-%d %H:%M:%S'),
            distancia=request.json['distancia'],
            tiempo=request.json['tiempo'],
            calorias=request.json['calorias'],
            usuario_id=request.json['usuario_id']
        )
        db.session.add(new_entrenamiento)
        db.session.commit()
        args = (new_entrenamiento.id, new_entrenamiento.fecha, new_entrenamiento.distancia, new_entrenamiento.tiempo, new_entrenamiento.calorias, new_entrenamiento.usuario_id)
        send_entrenamiento.apply_async(args=args, queue='logs')
        return entrenamiento_schema.dump(new_entrenamiento)