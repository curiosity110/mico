from django.test import TestCase
from django.urls import reverse


class IndexViewTests(TestCase):
    def test_index_page_returns_success(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_products_page_returns_success(self):
        response = self.client.get(reverse("products"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "all_products.html")

