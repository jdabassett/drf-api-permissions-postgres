from django.urls import path

from .views import SnackCreate, SnackUpdate, SnackView

urlpatterns = [
    path("view/", SnackView.as_view(), name="snack_view"),
    path("create/", SnackCreate.as_view(), name="snack_create"),
    path("update/<int:pk>/", SnackUpdate.as_view(), name="snack_update"),
]