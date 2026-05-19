import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Car, CarLike


class LikeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close(code=4001)
            return
        await self.accept()
        await self.channel_layer.group_add("likes_global", self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("likes_global", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        car_id = data.get('car_id')
        if not car_id: return

        is_liked, total_count = await self.toggle_like(car_id)

        # 🔹 Личное сообщение (только тому, кто нажал)
        await self.channel_layer.group_send(
            "likes_global",
            {
                "type": "send_color",
                "action": "personal_color",
                "car_id": car_id,
                "is_liked": is_liked,
                "count": total_count,
                "target_channel": self.channel_name,
            }
        )

        # 🔸 Публичное сообщение (всем остальным)
        await self.channel_layer.group_send(
            "likes_global",
            {
                "type": "send_count",
                "action": "public_count",
                "car_id": car_id,
                "count": total_count,
            }
        )

    async def send_color(self, event):
        # Отправляем только initiator'у
        if event.get("target_channel") == self.channel_name:
            await self.send(text_data=json.dumps(event))

    async def send_count(self, event):
        # Отправляем всем
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def toggle_like(self, car_id):
        car = Car.objects.get(id=car_id)
        like = CarLike.objects.filter(car=car, user=self.user).first()

        if like:
            like.delete()
            is_liked = False
        else:
            CarLike.objects.create(car=car, user=self.user)
            is_liked = True

        total_count = CarLike.objects.filter(car=car).count()
        return is_liked, total_count