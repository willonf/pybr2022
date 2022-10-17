from django.apps import AppConfig


# TODO: aqui configuramos as propriedades das aplicações criadas.
class BasicConfig(AppConfig):
    # Tipo implícito de chave primária para adição aos modelos deste app.
    default_auto_field = 'django.db.models.BigAutoField'
    # "Name" define a qual aplicação essa configuração se aplica
    name = 'basic'
    # Nome "Human-readable" da aplicação
    verbose_name = 'Basic'

    # TODO: Sobrescrita do método ready() para os receivers serem carregados
    def ready(self):
        import basic.receivers
        super(BasicConfig, self).ready()
