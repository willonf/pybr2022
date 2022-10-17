from django.db import connections, OperationalError
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


# TODO: função para executar strings de consultas SQL (atenção para SQL Injections)
# Útil para buscas 'extremamente' complexas ou que não seja possível realizar com o Django
# ATENÇÃO: É provável que, com muito esforço, seja possível realizar um SQL Injection,
# passando uma "query" como parametro
# Para evitar SQL Injections, é usar o método raw do manager odne se está realizando a busca. Ex.:
# queryset = models.Sale.objects.raw('STRING SQL'). Para obter o resultado, iterar em cima de queryset.query
def execute_query(query: str, many=True):
    """
    Função para executar strings de consultas SQL
    """
    try:
        # default: nome da conexão com o database no settings.py
        cursor = connections['default'].cursor()
        cursor.execute(query)
        result = cursor.fetchall()  # fetchall(): realiza a consulta de fato no banco

        columns = [column[0] for column in cursor.description]  # description: nome das colunas
        rows = [dict(zip(columns, row)) for row in result]
        return rows if many else rows[0] if len(rows) > 0 else None
    except OperationalError:
        raise Exception('Query error')


def send_channel_message(group: str, content: dict):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(group, {
        'type': 'group.message',
        'content': content
    })
