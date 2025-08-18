from django.urls import path
from . import views
from core.views import ProductPageFormView, ThankYouView, TestView

app_name = "core"
urlpatterns = [
    path('', views.index, name='index'),
<<<<<<< HEAD
    path('products/', views.products_page, name='products'),
=======
    path(
        "product-page/<slug:slug>/",
        ProductPageFormView.as_view(),
        name="product-page",
    ),
    path("thank-you/", ThankYouView.as_view(), name="thank-you"),
    path("test/", TestView.as_view(), name="test"),
>>>>>>> 90dfcbf (backend)
]
