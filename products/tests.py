from django.test import TestCase
from rest_framework.test import APIClient

from .models import Product


class ProductSearchApiTests(TestCase):
    def setUp(self):
        Product.objects.create(name="Alpha", slug="alpha", sale_price=10, stock_price=12, stock=1)
        Product.objects.create(name="Beta", slug="beta", sale_price=10, stock_price=12, stock=1)

    def test_search_filter_q(self):
        client = APIClient()
        resp = client.get("/api/products/", {"q": "alp"})
        self.assertEqual(resp.status_code, 200)
        names = [p["name"] for p in resp.json()["results"]]
        self.assertIn("Alpha", names)
        self.assertNotIn("Beta", names)
