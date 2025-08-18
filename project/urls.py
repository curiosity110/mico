from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

from products.views import ProductSearchApiView


urlpatterns = [
    path('admin/', admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("api/products/", ProductSearchApiView.as_view(), name="product-search"),
]

urlpatterns += i18n_patterns(
    path('', include('core.urls')),
    path('products/', include('products.urls')),
    prefix_default_language=False,
)
