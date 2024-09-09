import dis
from django.urls import path
from rest_framework import routers

from main.views import overridden_room_rate, room_rate, discount

app_name = "main"
main_router = routers.SimpleRouter()

room_rate_router = main_router.register(
    r"room-rates", room_rate.RoomRateViewSet, basename="room-rate"
)
overridden_room_rate_router = main_router.register(
    r"overridden-room-rates",
    overridden_room_rate.OverriddenRoomRateViewSet,
    basename="overridden-room-rate",
)
discount_router = main_router.register(
    r"discounts", discount.DiscountViewSet, basename="discount"
)

urlpatterns = main_router.urls
