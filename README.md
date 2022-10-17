# Aula 01

## Ambiente

1. Instalar Django no ambiente principal do Python

        pip install django

2. Iniciar projeto Django

        django-admin startproject nome_do_projeto

3. Criar uma nova virtual enviroment e instalar o django nela, como no passo 1.

4. Gerar o arquivo requirements.txt

        pip freeze > requirements.txt

## Ciclo de request do Django

1. Requisição do cliente
2. URL's
3. Viewsets
4. Serializers
5. Models

## Models

- Representam as entidades do banco de dados
- Cada módulo do django representa uma aplicação;
- Cada modelo é uma classe que herda de models.Model
- Cada app novo deve ser declarado no settings.py do projeto:

        nomeDoApp.apps.nomeDoAppConfig

## CLI Commands:

- Iniciar projeto Django

        django-admin startproject nome_do_projeto


- Criar um novo app:

        python manage.py startapp nome_da_aplicação


- Criar migrations:

        python manage.py makemigrations
        python manage.py makemigrations nome_do_app --empty (vazia)


- Verificar e listar as migrations:

        python manage.py showmigrations


- Rodar as migrations:

        python manage.py migrate
        python manage.py migrate nomde_app 0002_auto_20220329_2115 (específica)


- Realizar dump data para uso no loaddata (precisa estar populado com algum dado):

        python manage.py dumpdata nome_app.Model > path_arquivo.json (ou .yaml)
        python manage.py dumpdata nome_app.Model -o path_arquivo.json (ou .yaml)
        Ex.: python manage.py dumpdata basic.MaritalStatus > ./"Data Migration"/marital_status.json

## Receivers

- São gatilhos (triggers) que são ativados antes ou depois de uma operação sobre os modelos;
- São mecanismos síncronos


## Tarefas assíncronas com Celery e Redis
- Redis: message broker usado para se comunicar com o Celery
- Celery:  sistema de distribuição de tarefas
- Gevent: gerenciador de thread pools (nativo no linux)
- Para iniciar um worker (com o Redis up):
Obs.: A flag --pool é obrigatório no Windows 
        
        celery -A sale worker --loglevel=INFO --pool=gevent -Q default
        celery -A sale worker --loglevel=DEBUG --pool=gevent -Q default
        celery -A sale worker --loglevel=DEBUG --pool=gevent -Q default --concurrency=10


## Websoscket
- Biblioteca websocket client: websocket-client
- Utilizado em chats, notificações