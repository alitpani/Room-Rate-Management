from rest_framework import serializers
from main.models import Discount
from django.db.transaction import atomic
from main.services import DiscountService
from main.selectors import DiscountSelector


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = "__all__"

    @atomic
    def create(self, validated_data):
        """
        Create a new Discount using the DiscountService.
        """
        return DiscountService.create_discount(validated_data)

    @atomic
    def update(self, instance, validated_data):
        """
        Update an existing Discount using the DiscountService.
        """
        return DiscountService.update_discount(instance, validated_data)
