from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from kombu import Exchange, Queue

# TODO: configurações do Celery para
# Muitas tarefas independentes entre si ou que exigem muito processamento: o ideal é criar uma fila para cada atividade

# Configurações para o celery acessar os recursos do Django
# Variável de ambiente do serviço:
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sale.settings')

app = Celery('sale')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Configurações das filas
app.conf.task_queues = (
    Queue(name='default', exchange=Exchange('default'), routing_key='default'),
    Queue(name='periodic', exchange=Exchange('periodic'), routing_key='periodic'),
)

TASKS = {
    'period_task': {  # Por convenção, usamos o mesmo nome da task
        'task': 'basic.tasks.periodic_task',
        'schedule': 10  # 10 segundos
    }
}

# Configuração da tarefa periódica
app.conf.beat_schedule = TASKS

app.autodiscover_tasks()  # Vai carregar as tasks do projeto automaticamente
app.conf.timezone = 'America/Manaus'
