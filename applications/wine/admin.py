from django.contrib import admin
from .models import Wine, WineImage


class WineImageInline(admin.TabularInline):
    model = WineImage
    extra = 1


@admin.register(Wine)
class WineAdmin(admin.ModelAdmin):
    inlines = [WineImageInline]
