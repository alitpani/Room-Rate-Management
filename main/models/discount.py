from django.db import models


class Discount(models.Model):
    FIXED = "fixed"
    PERCENTAGE = "percentage"
    DISCOUNT_TYPE_CHOICES = [
        (FIXED, "Fixed"),
        (PERCENTAGE, "Percentage"),
    ]

    discount_id = models.AutoField(primary_key=True)
    discount_name = models.CharField(max_length=100)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.discount_name} - {self.discount_type} ({self.discount_value})"
