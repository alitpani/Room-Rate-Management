from main.models import OverriddenRoomRate


class OverriddenRoomRateService:
    @staticmethod
    def create_overridden_rate(data):
        """
        Service to create a new overridden room rate with validation.
        """
        overridden_rate = OverriddenRoomRate.objects.create(**data)
        return overridden_rate

    @staticmethod
    def update_overridden_rate(overridden_rate: OverriddenRoomRate, validated_data):
        """
        Service to update an existing overridden room rate with validation.
        """
        overridden_rate_value = validated_data.get("overridden_rate")
        stay_date = validated_data.get("stay_date")

        if overridden_rate_value is not None:
            overridden_rate.overridden_rate = overridden_rate_value
        if stay_date is not None:
            overridden_rate.stay_date = stay_date

        overridden_rate.full_clean()
        overridden_rate.save()
        return overridden_rate
