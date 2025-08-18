from django.test import TestCase
from django.urls import reverse


class IndexViewTests(TestCase):
    def test_index_page_returns_success(self):
        response = self.client.get(reverse("core:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_products_page_returns_success(self):
        response = self.client.get(reverse("products:product-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/list.html")

