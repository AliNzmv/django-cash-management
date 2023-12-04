from django.contrib import admin
from .models import User
from credit_management.models import Credit

class CreditInline(admin.StackedInline):
    model = Credit
    extra = 0
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name']
    inlines = [CreditInline]

