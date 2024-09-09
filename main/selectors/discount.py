from main.models import Discount


class DiscountSelector:

    @staticmethod
    def list_discounts(request):
        """
        Returns a queryset of all Discounts.
        """
        return Discount.objects.all()

    @staticmethod
    def get_discount(discount_id):
        """
        Returns a single Discount by ID.
        """
        return Discount.objects.filter(discount_id=discount_id).first()
