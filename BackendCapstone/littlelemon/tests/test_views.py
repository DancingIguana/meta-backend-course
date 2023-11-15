import datetime
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from restaurant import models, serializers

class MenuViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        models.Menu.objects.create(
            title="Pizza",
            price=200,
            inventory=5
        )
        models.Menu.objects.create(
            title="IceCream",
            price=80,
            inventory=5
        )
        models.Menu.objects.create(
            title="Cake",
            price=120,
            inventory=10
        )
    def test_getall(self):
        url = reverse("menu")
        response = self.client.get(url)
        expected = serializers.MenuSerializer(
            models.Menu.objects.all(), 
            many=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.data, expected.data)