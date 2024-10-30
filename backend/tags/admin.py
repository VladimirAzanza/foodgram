from django.contrib import admin

from tags.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug',
    )
    list_editable = (
        'name',
        'slug',
    )
    search_fields = (
        'id',
        'name',
        'slug'
    )
