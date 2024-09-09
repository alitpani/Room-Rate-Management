from django.db import models


# class RoomRate(models.Model):
#     room_id = models.IntegerField(unique=True)
#     room_name = models.CharField(max_length=100)
#     default_rate = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return (
#             f"{self.room_name} (ID: {self.room_id}) - Default Rate: {self.default_rate}"
#         )


class RoomRate(models.Model):
    room_id = models.IntegerField(unique=True)
    room_name = models.CharField(max_length=100)
    default_rate = models.DecimalField(max_digits=10, decimal_places=2)
    discounts = models.ManyToManyField("Discount", related_name="room_rates")

    def __str__(self):
        return (
            f"{self.room_name} (ID: {self.room_id}) - Default Rate: {self.default_rate}"
        )
