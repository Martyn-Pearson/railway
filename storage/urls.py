from django.urls import path
from . import views
from .views import IndexView, UpdateView

app_name = "storage"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("update/<int:location_id>/", UpdateView.as_view(), name="update"),
]