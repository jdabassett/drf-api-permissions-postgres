from django.contrib.auth import get_user_model
from django.db import models


class SnackCollection(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    snacks = models.ManyToManyField("snacks.Snack", blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
