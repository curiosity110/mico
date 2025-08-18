from django.urls import path

from order_imports.views import CreateXlsxOrderImportView, ListOrderImportsView, RetrieveOrderImportView, \
    AssignOrderImportToAgentView

urlpatterns = [
    path("xlsx/", CreateXlsxOrderImportView.as_view(), name="create_xlsx_order_import"),
    path("", ListOrderImportsView.as_view(), name="list_order_imports"),
    path("<int:pk>/", RetrieveOrderImportView.as_view(), name="retrieve_order_import"),
    path("<int:pk>/assign-agent/<int:agent_id>/", AssignOrderImportToAgentView.as_view(), name="assign-order-import-to-agent"),
]
