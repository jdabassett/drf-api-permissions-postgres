from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import SnackCollection
from .serializer import SnackCollectionSerializer


class SnackCollectionView(generics.ListAPIView):
    queryset = SnackCollection.objects.all()
    serializer_class = SnackCollectionSerializer


class SnackCollectionCreate(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = SnackCollection.objects.all()
    serializer_class = SnackCollectionSerializer


class SnackCollectionUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = SnackCollection.objects.all()
    serializer_class = SnackCollectionSerializer
