from django.contrib import admin

# Register your models here.
from vapor_manager.clients.models import Client, ClientNote


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass


@admin.register(ClientNote)
class ClientNoteAdmin(admin.ModelAdmin):
    pass
