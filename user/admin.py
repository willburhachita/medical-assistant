from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Permission
from user.models import *


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = UserChangeForm.Meta.fields


class UserAdminView(UserAdmin):
    form = CustomUserChangeForm
    add_form = UserCreationForm
    list_display = ('id', 'username', 'wallet_address', 'is_active', "is_superuser",)
    ordering = ("-id", )
    search_fields = ('id', 'username', 'email_address', 'wallet_address') 


    # fieldsets = (
    #     (None, {'fields': ('email_address', 'password', "game_balance","locked_balance", "bonus_balance", "xp_level", "xp_total_points", "xp_progress_points")}),
    #     ('Personal info', {'fields': ('username',"wallet_address", "full_name", "phone_number", "street_name",)}),
    #     ('Permissions', {'fields': ('verified','is_active', 'is_staff', 'is_superuser',
    #                                    'groups', 'user_permissions')}),
    #     ('Important dates', {'fields': ('last_login', 'date_joined')}),
    # )



admin.site.register(Permission)
admin.site.register(User, UserAdminView)
