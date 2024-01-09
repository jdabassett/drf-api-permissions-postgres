from django.contrib import admin

from .models import SnackCollection


class SnackCollectionAdmin(admin.ModelAdmin):
    list_display = ["owner"]


admin.site.register(SnackCollection, SnackCollectionAdmin)
