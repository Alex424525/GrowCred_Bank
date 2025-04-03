from django.contrib import admin

from transactions.models import DepositModel, WithdrawalModel

admin.site.register(DepositModel)
admin.site.register(WithdrawalModel)

