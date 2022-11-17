from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('id', 'email', 'is_admin', 'is_teacher', 'is_student', 'is_active',)
    list_filter = ('email', 'is_admin', 'is_teacher', 'is_student', 'is_active',)
    fieldsets = (
        (None, {'fields': ('first_name', 'email', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'is_teacher', 'is_student', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'is_teacher', 'is_student', 'is_admin', 'is_active')}
        ),
    )
    search_fields = ('id', 'email',)
    ordering = ('id', 'email',)


admin.site.register(User, CustomUserAdmin)
'''
admin.site.register(User)
'''