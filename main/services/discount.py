from main.models import Discount


class DiscountService:

    @staticmethod
    def create_discount(validated_data):
        """
        Creates a new Discount.
        """
        return Discount.objects.create(**validated_data)

    @staticmethod
    def update_discount(instance, validated_data):
        """
        Updates an existing Discount.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    @staticmethod
    def delete_discount(discount_id):
        """
        Deletes a Discount by its ID.
        """
        Discount.objects.filter(discount_id=discount_id).delete()
