from time import sleep

from basic import models, helpers


class SaleActions:
    @staticmethod
    def sale_by_year():
        results = models.SaleItem.objects.sold_by_year()
        counter = results.count()
        results = map(lambda item: f"{item['year']} - R$ {item['subtotal']};\n", results)
        with open('sale_by_year.txt', 'a') as file:
            for index, row in enumerate(results):
                file.write(row)
                percentage = (index + 1 / counter) * 100
                helpers.send_channel_message(group='chat', content={'message': f'{percentage}%'})
                sleep(0.5)
