from celery import Celery
from os import getenv

from zdravomil.core import Zdravomil

redis_host = getenv('REDIS_SERVICE_HOST', 'redis')
redis_port = getenv('REDIS_SERVICE_PORT', '6379')
redis_db = getenv('REDIS_SERVICE_DB', '0')
redis_url = "redis://{host}:{port}/{db}".format(host=redis_host, port=redis_port, db=redis_db)

# http://docs.celeryproject.org/en/latest/reference/celery.html#celery.Celery
app = Celery(backend=redis_url,
              broker=redis_url)


@app.task(name="task.zdravomil.run_linters_pr")
def run_linters(message):
    zdravo = Zdravomil()
    zdravo.message = message
    zdravo.artifact_info = {
        'repo': message['msg']['repository']['full_name'],
        'pr_id': message['msg']['issue']['number']
    }
    return zdravo.process()
