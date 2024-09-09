from django.db import models
from .room_rate import RoomRate
from .discount import Discount


class DiscountRoomRate(models.Model):
    room_rate = models.ForeignKey(RoomRate, on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)

    def __str__(self):
        return f"Discount {self.discount.discount_name} applied to {self.room_rate.room_name}"
