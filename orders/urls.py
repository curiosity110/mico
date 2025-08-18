from django.urls import path

from order_imports.views import AssignOrderImportToAgentView
from .views import (
    OrderListView,
    UpdateOrderStatusView,
    UpdateOrderAgentView,
    RetrieveOrderView,
    ConfirmOrderView,
    AddCommentView,
)

urlpatterns = [
    path("", OrderListView.as_view(), name="order-list"),
    path("<int:pk>/", RetrieveOrderView.as_view(), name="order-detail"),
    path("<int:pk>/status/", UpdateOrderStatusView.as_view(), name="order-detail"),
    path("<int:pk>/agent/", UpdateOrderAgentView.as_view(), name="order-agent"),
    path("<int:pk>/confirm/", ConfirmOrderView.as_view(), name="order-confirm"),
    path("<int:pk>/add-comment/", AddCommentView.as_view(), name="order-comment"),

]
