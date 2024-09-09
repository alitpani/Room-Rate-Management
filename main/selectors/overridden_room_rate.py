from main.models import OverriddenRoomRate
from django.db.models import Q


class OverriddenRoomRateSelector:
    @staticmethod
    def list_overridden_rates(request):
        """
        Selector to get a list of all overridden room rates, with optional filtering by room rate.
        """
        _filter = Q()
        if "room_rate_id" in request.query_params:
            _filter &= Q(room_rate_id=request.query_params["room_rate_id"])
        return OverriddenRoomRate.objects.filter(_filter)

    @staticmethod
    def get_overridden_rate_by_id(overridden_rate_id):
        """
        Selector to get a specific overridden room rate by id.
        """
        return OverriddenRoomRate.objects.filter(id=overridden_rate_id).first()
