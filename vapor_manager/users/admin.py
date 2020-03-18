from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from vapor_manager.users.forms import UserChangeForm, UserCreationForm
from vapor_manager.users import models

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("name",)}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]


class AccountNoteInline(admin.StackedInline):
    """ Adds inline for assigning Notes to Account """
    model = models.AccountNote
    extra = 0


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    """admin for Accounts"""
    list_display = ['owner', 'users']
    search_fields = ('company', 'owner__email',)
    filter_horizontal = ('groups', 'permissions',)
    inlines = [
        AccountNoteInline,
    ]

    def users(self, obj):
        return obj.users.count()
    users.short_description = 'Total Users'


@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    """admin for Groups"""
    list_display = (
        'name',
    )
    filter_horizontal = ('permissions',)


@admin.register(models.Permission)
class PermissionAdmin(admin.ModelAdmin):
    pass
