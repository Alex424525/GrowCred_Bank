from django.contrib import admin
from .models import Account, Transaction

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'bank_name', 'user', 'balance', 'is_active', 'created_at')
    list_filter = ('bank_name', 'is_active')
    search_fields = ('account_number', 'user__username')
    readonly_fields = ('account_number', 'created_at', 'updated_at')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'amount', 'transaction_type', 'description', 'created_at')
    search_fields = ('account__account_number', 'description')
    list_filter = ('transaction_type', 'created_at')