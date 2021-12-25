from django.urls import path

from . import views

app_name = "credit_cwallet"

urlpatterns = [
    path("", views.CreditCwalletListCreateView.as_view(), name="credit_cwallet")
]
