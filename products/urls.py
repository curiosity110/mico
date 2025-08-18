from django.urls import path

from products.views import  ProductListCreateView, ProductRetrieveUpdateView

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list-create'),
    path('<int:pk>/', ProductRetrieveUpdateView.as_view(), name='product-retrieve-update'),
]
