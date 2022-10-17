import imp
from channels.generic.websocket import AsyncJsonWebsocketConsumer


# TODO: Classes que representam os canais websocket


class ChatConsumer(AsyncJsonWebsocketConsumer):
    # Método chamado na conexão
    async def connect(self):
        # print(f'Client connected: {self.scope}')
        print(f'Client connected!')
        await self.accept()  # Aceita conexões socket
        # Criação do canal 'chat'
        await self.channel_layer.group_add('chat', self.channel_name)

    # Método chamado ao encerrar-se a conexão
    async def disconnect(self, code):
        await self.channel_layer.group_discard('chat', self.channel_name)

    # Método para enviar mensagens
    async def group_message(self, event):
        await self.send_json(content=event['content'])

    # Método para receber mensagens
    async def receive_json(self, event, **kwargs):  # Padrão da superclasse
        await self.channel_layer.group_send('chat', {
            'type': 'group.message',
            'content': event
        })
