from django.db import models

# Create your models here.
class PaymentMethod(models.Model):
    coin_name = models.CharField(max_length=100)
    coin_address = models.CharField(max_length=200)
    coin_qr_code = models.ImageField(blank=True, null=True)
    enable = models.BooleanField(default=True)