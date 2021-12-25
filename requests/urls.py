from django.urls import path

from . import views

app_name = 'requests'

urlpatterns = [
    path('import_users_request/', views.ImportUserRequestView.as_view(), name="import_users_request"),
    path('celery/', views.celery, name="celery"),
]
