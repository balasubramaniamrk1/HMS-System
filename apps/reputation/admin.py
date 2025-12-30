from django.contrib import admin
from .models import Platform, Review

@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'platform', 'rating', 'review_date', 'is_featured')
    list_filter = ('platform', 'rating', 'is_featured')
    search_fields = ('author_name', 'content')
    list_editable = ('is_featured',)
