from main.models import RoomRate
from rest_framework.request import Request as DRFRequest
from django.db.models import Q


class RoomRateSelector:
    @staticmethod
    def list_room_rates(request: DRFRequest):
        """
        Selector to get a list of all room rates.
        """
        _filter = Q()
        if "room_id" in request.query_params:
            _filter &= Q(room_id=request.query_params["room_id"])
        return RoomRate.objects.filter(_filter)

    @staticmethod
    def get_room_rate_by_room_id(room_id):
        """
        Selector to get a specific room rate by id.
        """
        return RoomRate.objects.filter(room_id=room_id).first()

    @staticmethod
    def get_room_rate(room_rate_id):
        """
        Selector to get a specific room rate by id.
        """
        return RoomRate.objects.filter(id=room_rate_id).first()
