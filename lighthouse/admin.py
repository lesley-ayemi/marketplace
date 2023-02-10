from django.contrib import admin
from .models import PaymentMethod, SendEmailUser
# Register your models here.

admin.site.register(PaymentMethod)
admin.site.register(SendEmailUser)