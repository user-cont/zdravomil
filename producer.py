#!/usr/bin/python3

import os
import celery
import time

if __name__ == '__main__':
    redis_host = os.getenv('REDIS_SERVICE_HOST', 'redis')
    redis_port = os.getenv('REDIS_SERVICE_PORT', '6379')
    redis_db = os.getenv('REDIS_SERVICE_DB', '0')
    redis_url = "redis://{host}:{port}/{db}".format(host=redis_host, port=redis_port, db=redis_db)

    # http://docs.celeryproject.org/en/latest/reference/celery.html#celery.Celery
    c = celery.Celery(backend=redis_url,
               broker=redis_url)
    # Define which tasks go to which queue
    c.conf.update(
        task_routes={
            'task.zdravomil.run_linters_pr': {'queue': 'queue.zdravomil'}
        }
    )
    message = {
  'topic': 'org.fedoraproject.prod.github.issue.comment',
  'msg': {
    'issue': {
      'number': 2,
      'pull_request': {
        'url': 'https://api.github.com/repos/container-images/rsyslog/pulls/2'
      }
    },
    'repository': {
      'full_name': 'container-images/rsyslog',
    }
  }
}
    result1 = c.send_task(name='task.zdravomil.run_linters_pr',
                            kwargs={'message': message})

    # Give Celery some time to pick up the message from queue and run the task
    time.sleep(2)
    print('Task1 finished? ', result1.ready())
    print('Task1 result: ', result1.result)
