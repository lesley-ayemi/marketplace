from django.db import models
from cloudinary.models import CloudinaryField
from mutual.models import TimeStampedModel
# Create your models here.
class PaymentMethod(TimeStampedModel):
    class PaymentType(models.TextChoices):
        MINTING = 'minting'
        DEPOSIT = 'deposit'
    coin_name = models.CharField(max_length=100)
    coin_address = models.CharField(max_length=200)
    coin_qr_code = models.FileField(null=True, blank=True)
    coin_network = models.CharField(max_length=300, blank=True, null=True, default='')
    wallet_type = models.CharField(max_length=30, choices=PaymentType.choices, default='deposit')
    enable = models.BooleanField(default=True)
    
    def __str__(self):
        return self.coin_name
    
    
class SendEmailUser(TimeStampedModel):
    email = models.EmailField(max_length=200, blank=True, null=True)
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField(null=True, blank=True)
    files = models.FileField(blank=True, null=True)