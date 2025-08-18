from django.urls import path
from . import views
from core.views import (
    ProductPageFormView,
    ThankYouView,
    TestView,
    AboutView,
    FAQView,
    ContactView,
)

app_name = "core"
urlpatterns = [
    path('', views.index, name='index'),
    path(
        "product-page/<slug:slug>/",
        ProductPageFormView.as_view(),
        name="product-page",
    ),
    path("thank-you/", ThankYouView.as_view(), name="thank-you"),
    path("test/", TestView.as_view(), name="test"),
    path("about/", AboutView.as_view(), name="about"),
    path("faq/", FAQView.as_view(), name="faq"),
    path("contact/", ContactView.as_view(), name="contact"),
]
