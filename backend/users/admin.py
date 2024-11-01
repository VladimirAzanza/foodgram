from django.contrib import admin

from users.models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ('user_permissions',)
    list_display = (
        'id',
        'first_name',
        'last_name',
        'email',
        'username',
        'is_staff',
        'date_joined'
    )
    search_fields = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name'
    )
    list_editable = (
        'is_staff',
    )
    list_filter = (
        'is_staff',
        'date_joined'
    )
