# serializers.py
import re
from rest_framework import serializers
from main.models import RoomRate
from main.models.discount import Discount
from main.serializers.discount import DiscountSerializer
from main.services.room_rate import RoomRateService
from main.selectors.room_rate import RoomRateSelector
from django.db.transaction import atomic


class RoomRateSerializer(serializers.ModelSerializer):
    discounts = DiscountSerializer(many=True, read_only=True)

    class Meta:
        model = RoomRate
        fields = "__all__"

    @atomic
    def create(self, validated_data):
        """
        Create a new RoomRate using the RoomRateService.
        """
        return RoomRateService.create_room_rate(validated_data)

    @atomic
    def update(self, instance, validated_data):
        """
        Update an existing RoomRate using the RoomRateService.
        """
        return RoomRateService.update_room_rate(instance, validated_data)


class RoomRateDiscountMappingSerializer(serializers.Serializer):
    room_rate_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )
    discount_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )

    def create(self, validated_data):
        room_rate_ids = validated_data["room_rate_ids"]
        discount_ids = validated_data["discount_ids"]

        room_rates = RoomRate.objects.filter(id__in=room_rate_ids)
        discounts = Discount.objects.filter(id__in=discount_ids)

        # Apply the discounts to each room rate
        for room_rate in room_rates:
            room_rate.discounts.add(*discounts)

        return {
            "room_rate_ids": room_rate_ids,
            "discount_ids": discount_ids,
        }
