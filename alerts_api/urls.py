from django.urls import path
from .views import *


urlpatterns = [
    path('fetch-all/', fetch_all, name="fetch-all-alerts"),
    path('create/', create_alert, name="create-alert"),
    path('delete/<int:pk>', delete_alert, name="delete-alert"),
]


