from celery import Celery
from app import app

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task
def delete_album_task(album_id):
    album_path = os.path.join('albums', album_id)
    if os.path.exists(album_path):
        shutil.rmtree(album_path)
        return {"status": "Album deleted successfully"}
    else:
        return {"error": "Album not found"}
