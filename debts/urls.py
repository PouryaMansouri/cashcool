from django.urls import path

from . import views

app_name = "debt"

urlpatterns = [
    path("repayment/", views.DebtRepaymentView.as_view(), name="debt_repayment")
]

urlpatterns = urlpatterns + [
    path("", views.DebtListView.as_view(), name="all_debt"),
    path("<int:pk>/", views.DebtRetrieveView.as_view(), name="one_debt"),
    path("penalty/", views.DebtPenaltyListView.as_view(), name="one_debt"),
    path("penalty/<int:pk>/", views.DebtPenaltyRetrieveView.as_view(), name="one_debt"),

]
