# TODO: Receivers

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from basic import models


# Sempre que um estado for cadastrado, a função abaixo será executada
# signal: lista com os tipos de operações. Ex.: [post_save, post_delete, pre_save]
# sender: modelo a ser utilizado
# dispatch_uid: id único do receiver (pode ser o nome da função)
# weak: o padrão é True. Previne que o garbage collector limpe um receiver antes de ser executado
@receiver(signal=post_save, sender=models.State, dispatch_uid='create_file_state', weak=False)
def create_file_state(instance, **kwargs):
    # instance: instância do objeto que foi operado
    # kwargs: possui informações úteis sobre a operação
    with open('states.txt', 'a') as file:
        file.write(f'{instance.id} | {instance.name}\n')


# pre_save: antes de salvar
@receiver(signal=[pre_save], sender=models.SaleItem, dispatch_uid='update_sale_item_price', weak=False)
def update_sale_item_price(instance, **kwargs):
    instance.product_price = instance.product.sale_price
