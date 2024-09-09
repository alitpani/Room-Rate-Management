# services.py
from decimal import Decimal
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from main.models import RoomRate
from main.models.discount import Discount
from main.models.overridden_room_rate import OverriddenRoomRate
from main.selectors.room_rate import RoomRateSelector


class RoomRateService:
    @staticmethod
    def create_room_rate(data):
        """
        Service to create a new room rate with validation.
        """
        room_rate = RoomRate.objects.create(**data)
        return room_rate

    @staticmethod
    def update_room_rate(room_rate: RoomRate, validated_data):
        """
        Service to update an existing room rate with validation.
        """
        room_id = validated_data.get("room_id")
        room_name = validated_data.get("room_name")
        default_rate = validated_data.get("default_rate")

        if room_id is not None:
            room_rate.room_id = room_id
        if room_name is not None:
            room_rate.room_name = room_name
        if default_rate is not None:
            room_rate.default_rate = default_rate

        room_rate.full_clean()
        room_rate.save()
        return room_rate

    @staticmethod
    def get_final_rate_for_date(room_rate, date):
        try:
            # Use the overridden rate if available
            override = OverriddenRoomRate.objects.get(
                room_rate=room_rate, stay_date=date
            )
            final_rate = override.overridden_rate
        except OverriddenRoomRate.DoesNotExist:
            # If no overridden rate exists, use the default rate
            final_rate = room_rate.default_rate

        # Apply the highest discount
        highest_discount = room_rate.discounts.order_by("-discount_value").first()

        if highest_discount:
            if highest_discount.discount_type == "fixed":
                final_rate = Decimal(final_rate) - Decimal(
                    highest_discount.discount_value
                )
            elif highest_discount.discount_type == "percentage":
                discount_amount = Decimal(final_rate) * (
                    Decimal(highest_discount.discount_value) / 100
                )
                final_rate = Decimal(final_rate) - discount_amount

        return final_rate


class RoomRateDiscountMappingService:

    @staticmethod
    def map_discounts_to_room_rates(room_rate_ids, discount_ids):
        """
        Maps multiple discounts to multiple room rates.
        """
        room_rates = RoomRate.objects.filter(id__in=room_rate_ids)
        discounts = Discount.objects.filter(discount_id__in=discount_ids)

        for room_rate in room_rates:
            room_rate.discounts.add(*discounts)

        return room_rates
