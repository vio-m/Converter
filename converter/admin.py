from django.contrib import admin
from .models import Video

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'typ', 'url')
    list_filter = ('title', 'typ', 'url')
    search_fields = ('title', 'typ', 'url')
