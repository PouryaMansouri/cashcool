from django.urls import path

from . import views

app_name = "demand"

urlpatterns = [
    path("", views.DemandListView.as_view(), name="all_debt"),
    path("<int:pk>/", views.DemandRetrieveView.as_view(), name="one_debt"),

]
