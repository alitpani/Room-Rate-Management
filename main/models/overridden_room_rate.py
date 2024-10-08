from django.db import models
from .room_rate import RoomRate


class OverriddenRoomRate(models.Model):
    room_rate = models.ForeignKey(RoomRate, on_delete=models.CASCADE)
    overridden_rate = models.DecimalField(max_digits=10, decimal_places=2)
    stay_date = models.DateField()

    def __str__(self):
        return f"Overridden Rate for {self.room_rate.room_name} on {self.stay_date}: {self.overridden_rate}"
