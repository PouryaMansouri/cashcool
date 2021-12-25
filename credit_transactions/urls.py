from django.urls import path

from . import views

app_name = "credit_transactions"

urlpatterns = [
    path("", views.CreditTransactionListCreateView.as_view(), name="transaction")
]
