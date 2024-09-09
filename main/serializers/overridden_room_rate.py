from rest_framework import serializers
from main.models import OverriddenRoomRate
from main.selectors.overridden_room_rate import OverriddenRoomRateSelector
from main.services import OverriddenRoomRateService
from django.db.transaction import atomic


class OverriddenRoomRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OverriddenRoomRate
        fields = "__all__"

    @atomic
    def create(self, validated_data):
        """
        Create a new OverriddenRoomRate using the OverriddenRoomRateService.
        """
        return OverriddenRoomRateService.create_overridden_rate(validated_data)

    @atomic
    def update(self, instance, validated_data):
        """
        Update an existing OverriddenRoomRate using the OverriddenRoomRateService.
        """
        return OverriddenRoomRateService.update_overridden_rate(
            instance, validated_data
        )

    # @classmethod
    # def list_overridden_rates(cls, request):
    #     """
    #     Get a list of all OverriddenRoomRates using the OverriddenRoomRateSelector.
    #     """
    #     return OverriddenRoomRateSelector.list_overridden_rates(request)
