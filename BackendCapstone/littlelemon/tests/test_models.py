from django.test import TestCase
from restaurant import models

class MenuTest(TestCase):
    def test_get_item(self):
        item = models.Menu.objects.create(
            title="IceCream", 
            price=80, 
            inventory=100
        )
        self.assertEqual(str(item), "IceCream : 80")