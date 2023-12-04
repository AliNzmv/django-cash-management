from django.contrib import admin
from .models import Credit, Transaction

class TransactionInline(admin.TabularInline):
    model = Transaction.credits.through
    extra = 0

@admin.register(Credit)
class CreditAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'balance', 'date_created']
    inlines = [TransactionInline]
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'status', 'money']
