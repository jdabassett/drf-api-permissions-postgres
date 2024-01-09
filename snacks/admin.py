from django.contrib import admin

from .models import Snack


class SnackAdmin(admin.ModelAdmin):
    list_display = ["owner", "name", "created_at"]


admin.site.register(Snack, SnackAdmin)
