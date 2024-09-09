from rest_framework import viewsets, serializers
from main.models import Discount
from main.serializers import DiscountSerializer
from main.selectors import DiscountSelector
from main.services import DiscountService


class DiscountViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing discounts.
    """

    lookup_url_kwarg = "discount_id"
    serializer_class = DiscountSerializer
    queryset = Discount.objects.all()
    serializer_classes_map = {
        "create": {"input": DiscountSerializer},
        "partial_update": {"input": DiscountSerializer},
    }

    def get_object(self):
        discount = DiscountSelector.get_discount(self.kwargs.get(self.lookup_url_kwarg))
        if discount is None:
            raise serializers.ValidationError("Discount not found")
        return discount

    def get_queryset(self):
        """
        Return a list of all discounts.
        """
        return DiscountSelector.list_discounts(self.request)

    def perform_destroy(self, instance):
        """
        Delete a discount.
        """
        DiscountService.delete_discount(instance.discount_id)
