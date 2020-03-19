from django.contrib import admin

# Register your models here.
from vapor_manager.accounts import models


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


@admin.register(models.AccountInvite)
class AccountInviteAdmin(admin.ModelAdmin):
    pass
