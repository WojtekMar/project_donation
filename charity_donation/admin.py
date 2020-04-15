from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, RegisterForm
from .models import CustomUser, Category, Institution, Donation

# Register your models here.
admin.site.register(Category)
admin.site.register(Institution)
admin.site.register(Donation)



class CustomUserAdmin(UserAdmin):
    add_form = RegisterForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active', 'first_name', 'last_name')
    list_filter = ('email', 'is_staff', 'is_active', 'first_name', 'last_name')
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password', 'repeat password', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)