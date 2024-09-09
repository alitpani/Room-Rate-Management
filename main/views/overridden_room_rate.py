from rest_framework import viewsets, serializers
from main.models import OverriddenRoomRate
from main.serializers import OverriddenRoomRateSerializer
from main.selectors import OverriddenRoomRateSelector
from main.services import OverriddenRoomRateService


class OverriddenRoomRateViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing, creating, updating, and deleting overridden room rates.
    """

    lookup_url_kwarg = "overridden_rate_id"
    serializer_class = OverriddenRoomRateSerializer
    queryset = OverriddenRoomRate.objects.all()
    serializer_classes_map = {
        "create": {"input": OverriddenRoomRateSerializer},
        "partial_update": {"input": OverriddenRoomRateSerializer},
    }

    def get_queryset(self):
        """
        Use OverriddenRoomRateSelector to return a filtered queryset.
        """
        return OverriddenRoomRateSelector.list_overridden_rates(self.request)

    def get_object(self):
        """
        Get an overridden room rate by id using the selector.
        """
        overridden_rate = OverriddenRoomRateSelector.get_overridden_rate_by_id(
            self.kwargs.get(self.lookup_url_kwarg)
        )
        if overridden_rate is None:
            raise serializers.ValidationError("Overridden rate not found")
        return overridden_rate

    def perform_destroy(self, instance):
        """
        Delete an overridden room rate.
        """
        instance.delete()

    def get_serializer_class(self):
        """
        Return the serializer class based on the action being performed.
        """
        if self.action in self.serializer_classes_map:
            return self.serializer_classes_map[self.action].get(
                "input", self.serializer_class
            )
        return self.serializer_class
