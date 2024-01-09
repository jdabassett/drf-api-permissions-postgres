from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import Snack
from .serializer import SnackSerializer


class SnackView(generics.ListAPIView):
    queryset = Snack.objects.all()
    serializer_class = SnackSerializer


class SnackCreate(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Snack.objects.all()
    serializer_class = SnackSerializer


class SnackUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser,)
    queryset = Snack.objects.all()
    serializer_class = SnackSerializer
