from django.urls import path

from .views import SnackCollectionCreate, SnackCollectionDetailed, SnackCollectionView

urlpatterns = [
    path("view/", SnackCollectionView.as_view(), name="snack_collection_view"),
    path("create/", SnackCollectionCreate.as_view(), name="snack_collection_list"),
    path("update/<int:pk>/", SnackCollectionDetailed.as_view(), name="snack_collection_detailed"),
]