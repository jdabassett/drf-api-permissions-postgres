from django.urls import path

from .views import SnackCollectionCreate, SnackCollectionUpdate, SnackCollectionView

urlpatterns = [
    path("view/", SnackCollectionView.as_view(), name="snack_collection_view"),
    path("create/", SnackCollectionCreate.as_view(), name="snack_collection_create"),
    path("update/<int:pk>/", SnackCollectionUpdate.as_view(), name="snack_collection_update"),
]