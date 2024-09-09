from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import RoomRate, OverriddenRoomRate, Discount
from decimal import Decimal
from datetime import date
from datetime import timedelta


class CommonSetupMixin:
    def setUp(self):
        # Create a test user and log them in
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")

        # Create a RoomRate object to use in OverriddenRoomRate tests
        self.room_rate = RoomRate.objects.create(
            room_id=1, room_name="Deluxe Suite", default_rate="200.00"
        )


class DiscountsAPITestCase(CommonSetupMixin, APITestCase):
    def test_get_discounts_list(self):
        url = reverse("main:discount-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), list)

    def test_create_discount(self):
        url = reverse("main:discount-list")
        data = {
            "discount_name": "Summer Sale",
            "discount_type": "fixed",
            "discount_value": "50.00",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["discount_name"], "Summer Sale")

    def test_get_discount_by_id(self):
        discount = Discount.objects.create(
            discount_name="Winter Sale",
            discount_type="percentage",
            discount_value="20.00",
        )
        url = reverse("main:discount-detail", args=[discount.discount_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["discount_id"], discount.discount_id)

    def test_update_discount(self):
        discount = Discount.objects.create(
            discount_name="Spring Sale", discount_type="fixed", discount_value="30.00"
        )
        url = reverse("main:discount-detail", args=[discount.discount_id])
        updated_data = {
            "discount_name": "Updated Sale",
            "discount_type": "percentage",
            "discount_value": "15.00",
        }
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["discount_name"], "Updated Sale")

    def test_partial_update_discount(self):
        discount = Discount.objects.create(
            discount_name="Autumn Sale", discount_type="fixed", discount_value="40.00"
        )
        url = reverse("main:discount-detail", args=[discount.discount_id])
        updated_data = {"discount_value": "25.00"}
        response = self.client.patch(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["discount_value"], "25.00")

    def test_delete_discount(self):
        discount = Discount.objects.create(
            discount_name="Flash Sale",
            discount_type="percentage",
            discount_value="10.00",
        )
        url = reverse("main:discount-detail", args=[discount.discount_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Discount.objects.filter(discount_id=discount.discount_id).exists()
        )


class OverriddenRoomRatesAPITestCase(CommonSetupMixin, APITestCase):
    def test_get_overridden_room_rates_list(self):
        url = reverse("main:overridden-room-rate-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), list)

    def test_create_overridden_room_rate(self):
        url = reverse("main:overridden-room-rate-list")
        data = {
            "overridden_rate": "150.00",
            "stay_date": "2024-09-10",
            "room_rate": self.room_rate.id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["overridden_rate"], "150.00")

    def test_get_overridden_room_rate_by_id(self):
        overridden_rate = OverriddenRoomRate.objects.create(
            overridden_rate="200.00", stay_date="2024-09-10", room_rate=self.room_rate
        )
        url = reverse("main:overridden-room-rate-detail", args=[overridden_rate.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], overridden_rate.id)

    def test_update_overridden_room_rate(self):
        overridden_rate = OverriddenRoomRate.objects.create(
            overridden_rate="150.00", stay_date="2024-09-10", room_rate=self.room_rate
        )
        url = reverse("main:overridden-room-rate-detail", args=[overridden_rate.id])
        updated_data = {
            "overridden_rate": "180.00",
            "stay_date": "2024-09-12",
            "room_rate": self.room_rate.id,
        }
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["overridden_rate"], "180.00")

    def test_delete_overridden_room_rate(self):
        overridden_rate = OverriddenRoomRate.objects.create(
            overridden_rate="150.00", stay_date="2024-09-10", room_rate=self.room_rate
        )
        url = reverse("main:overridden-room-rate-detail", args=[overridden_rate.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            OverriddenRoomRate.objects.filter(id=overridden_rate.id).exists()
        )


class RoomRatesAPITestCase(CommonSetupMixin, APITestCase):
    def test_get_room_rates_list(self):
        url = reverse("main:room-rate-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), list)

    def test_create_room_rate(self):
        url = reverse("main:room-rate-list")
        data = {"room_id": 2, "room_name": "Superior Suite", "default_rate": "300.00"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["room_name"], "Superior Suite")

    def test_get_room_rate_by_id(self):
        url = reverse("main:room-rate-detail", args=[self.room_rate.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.room_rate.id)

    def test_update_room_rate(self):
        url = reverse("main:room-rate-detail", args=[self.room_rate.id])
        updated_data = {
            "room_name": "Updated Deluxe Suite",
            "default_rate": "250.00",
            "room_id": self.room_rate.room_id,
        }
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["room_name"], "Updated Deluxe Suite")

    def test_delete_room_rate(self):
        url = reverse("main:room-rate-detail", args=[self.room_rate.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(RoomRate.objects.filter(id=self.room_rate.id).exists())


class FinalRoomRateCalculationTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        self.room_rate = RoomRate.objects.create(
            room_id=1, room_name="Test Room", default_rate="200.00"
        )

        # Create a fixed discount
        self.discount_fixed = Discount.objects.create(
            discount_name="Fixed Discount",
            discount_type="fixed",
            discount_value="20.00",
        )
        self.room_rate.discounts.add(self.discount_fixed)

        # Create a percentage discount
        self.discount_percentage = Discount.objects.create(
            discount_name="Percentage Discount",
            discount_type="percentage",
            discount_value="10.00",
        )
        self.room_rate.discounts.add(self.discount_percentage)

    def test_final_rate_without_overridden_rate(self):
        """
        Test that the final rate without any overridden rate applies the highest discount
        """
        final_rate = Decimal("200.00") - Decimal("20.00")  # Fixed discount should apply
        url = reverse("main:room-rate-rates-for-date-range")

        response = self.client.get(
            url,
            {
                "room_id": self.room_rate.room_id,
                "start_date": "2024-09-10",
                "end_date": "2024-09-10",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(response.data[0]["final_rate"]), final_rate)

    def test_final_rate_with_overridden_rate(self):
        """
        Test that the final rate applies the overridden rate and highest discount
        """
        OverriddenRoomRate.objects.create(
            room_rate=self.room_rate, overridden_rate="180.00", stay_date="2024-09-10"
        )

        final_rate = Decimal("180.00") - Decimal("20.00")  # Highest fixed discount
        url = reverse("main:room-rate-rates-for-date-range")

        response = self.client.get(
            url,
            {
                "room_id": self.room_rate.room_id,
                "start_date": "2024-09-10",
                "end_date": "2024-09-10",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(response.data[0]["final_rate"]), final_rate)

    def test_final_rate_with_percentage_discount(self):
        """
        Test that the percentage discount is applied correctly
        """
        self.room_rate.discounts.remove(self.discount_fixed)

        final_rate = Decimal("200.00") * Decimal("0.90")  # 10% off
        url = reverse("main:room-rate-rates-for-date-range")

        response = self.client.get(
            url,
            {
                "room_id": self.room_rate.room_id,
                "start_date": "2024-09-10",
                "end_date": "2024-09-10",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(response.data[0]["final_rate"]), final_rate)

    def test_final_rate_with_both_discounts(self):
        """
        Test that the highest discount (fixed or percentage) is applied
        """
        final_rate = Decimal("200.00") - Decimal("20.00")  # Fixed discount should apply
        url = reverse("main:room-rate-rates-for-date-range")

        response = self.client.get(
            url,
            {
                "room_id": self.room_rate.room_id,
                "start_date": "2024-09-10",
                "end_date": "2024-09-10",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(response.data[0]["final_rate"]), final_rate)

    def test_final_rate_without_any_discounts(self):
        """
        Test that the default rate is returned if no discounts are available
        """
        self.room_rate.discounts.clear()

        final_rate = Decimal("200.00")  # No discounts
        url = reverse("main:room-rate-rates-for-date-range")

        response = self.client.get(
            url,
            {
                "room_id": self.room_rate.room_id,
                "start_date": "2024-09-10",
                "end_date": "2024-09-10",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(response.data[0]["final_rate"]), final_rate)
