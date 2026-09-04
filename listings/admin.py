from django.contrib import admin
from .models import Advertisement

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    """Админка для объявлений."""
    list_display = ['id', 'title', 'status', 'creator', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']