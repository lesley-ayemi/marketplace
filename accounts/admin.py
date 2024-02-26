from django.contrib import admin
from .models import User, MoreDetails, UserWallet, UserTransactions, WithdrawalGasFee
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(User)
admin.site.register(MoreDetails)
admin.site.register(UserWallet)
admin.site.register(UserTransactions)
admin.site.register(WithdrawalGasFee)