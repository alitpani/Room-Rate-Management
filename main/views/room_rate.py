# serializers.py
from rest_framework import serializers, viewsets, status
from main.models import RoomRate
from main.selectors.room_rate import RoomRateSelector
from main.serializers.room_rate import (
    RoomRateDiscountMappingSerializer,
    RoomRateSerializer,
)
from main.services.room_rate import RoomRateDiscountMappingService, RoomRateService
from rest_framework.response import Response
from rest_framework.decorators import action
from datetime import datetime, timedelta


class RoomRateViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing room rates.
    """

    lookup_url_kwarg = "room_rate_id"
    serializer_class = RoomRateSerializer
    queryset = RoomRate.objects.all()
    serializer_classes_map = {
        "create": {"input": RoomRateSerializer},
        "partial_update": {"input": RoomRateSerializer},
        "map_discounts": {"input": RoomRateDiscountMappingSerializer},
    }

    def get_object(self):
        room_rate = RoomRateSelector.get_room_rate(
            self.kwargs.get(self.lookup_url_kwarg)
        )
        if room_rate is None:
            raise serializers.ValidationError("Room rate not found")
        return room_rate

    def get_queryset(self):
        """
        Optionally restricts the returned room rates.
        """
        return RoomRateSelector.list_room_rates(self.request)

    def perform_destroy(self, instance):
        """Delete Item Definition."""
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

    @action(detail=False, methods=["post"], url_path="map-discounts")
    def map_discounts(self, request):
        serializer = RoomRateDiscountMappingSerializer(data=request.data)
        if serializer.is_valid():
            RoomRateDiscountMappingService.map_discounts_to_room_rates(
                serializer.validated_data["room_rate_ids"],
                serializer.validated_data["discount_ids"],
            )
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path="rates-for-date-range")
    def rates_for_date_range(self, request):
        room_id = request.query_params.get("room_id")
        room_name = request.query_params.get("room_name")
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        # Input validation
        if not start_date or not end_date:
            return Response(
                {"error": "Please provide both start_date and end_date."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"error": "Invalid date format. Please use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Fetch the room rate by room ID or room name
        room_rate = None
        if room_id:
            room_rate = RoomRate.objects.filter(room_id=room_id).first()
        elif room_name:
            room_rate = RoomRate.objects.filter(room_name=room_name).first()

        if not room_rate:
            return Response(
                {"error": "Room not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # Calculate final rates for each day in the date range
        current_date = start_date
        rates = []
        while current_date <= end_date:
            final_rate = RoomRateService.get_final_rate_for_date(
                room_rate, current_date
            )
            rates.append({"date": current_date, "final_rate": final_rate})
            current_date += timedelta(days=1)

        return Response(rates, status=status.HTTP_200_OK)
