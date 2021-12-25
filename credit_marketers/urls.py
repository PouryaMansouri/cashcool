from django.urls import path

from . import views

app_name = "marketer"

urlpatterns = [
    path("", views.CreditMarketerListView.as_view(), name="marketer_list"),
    path("<int:pk>/", views.CreditMarketerRetrieveView.as_view(), name="marketer_detail")
]
