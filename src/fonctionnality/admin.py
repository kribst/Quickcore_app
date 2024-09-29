from django.contrib import admin
from .models import Stack, ChatMessage, CustomerUser, Visite


admin.site.index_title = 'Management'
class AdminCustomerUser(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'gender', 'email', 'country', 'phone_number', 'image',)
    search_fields = ('username', 'first_name', 'last_name', 'gender',)
    list_filter = ('gender', 'email',)
    list_per_page = 13

    empty_value = "empty"


class AdminStack(admin.ModelAdmin):
    list_display = ('title', 'user', 'assigned_to', 'status', 'duration', 'created_at', 'updated_at',)
    list_editable = ('user',)
    search_fields = ('title', 'user',)
    list_filter = ('status',)
    autocomplete_fields = ('user', 'assigned_to',)
    list_per_page = 13

    empty_value = "empty"


class AdminChatMessage(admin.ModelAdmin):
    list_display = ('user', 'message', 'timestamp',)
    search_fields = ['message', 'user__username']
    autocomplete_fields = ('user',)
    empty_value = "empty"
    list_per_page = 13


# Register your models here.
admin.site.register(Stack, AdminStack)
admin.site.register(ChatMessage, AdminChatMessage)
admin.site.register(CustomerUser, AdminCustomerUser)
admin.site.register(Visite)

