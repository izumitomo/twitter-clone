from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

# class AccountAdmin(UserAdmin):
#    model = Account
#    fieldsets = UserAdmin.fieldsets

admin.site.register(Account)
