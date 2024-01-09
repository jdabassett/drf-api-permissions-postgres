from rest_framework import serializers

from .models import SnackCollection


class SnackCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "owner", "snacks"]
        model = SnackCollection
