import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from mutual.models import TimeStampedModel
from lighthouse.models import PaymentMethod

class User(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    balance = models.FloatField(null=True, blank=True, default=0)
    is_admin = models.BooleanField(default=False)
    is_user = models.BooleanField(default=True)
    get_user_p = models.CharField(blank=True, null=True)
    profile_pic = models.FileField(blank=True, null=True, help_text='Upload a Profile Picture')
    cover_photo = models.FileField(blank=True, null=True, help_text='Upload a cover photo')
    

class MoreDetails(models.Model):
    GENDER_TYPE = (
        ('man', 'man'),
        ('woman', 'woman'),
        ('transgender', 'transgender'),
        ('non-binary/non-conforming', 'non-binary/non-comforming'),
        ('prefer-not-to-respond', 'prefer-not-to-respond'),
    )
    bio = models.TextField(blank=True, null=True)
    work_role = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=100, choices=GENDER_TYPE, default='')
    phone_number = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255, blank=True)
    
    
class UserWallet(models.Model):
    user_wallet = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='user_wallet')
    wallet_name = models.CharField(max_length=200)
    wallet_address = models.CharField(max_length=255)
    
    
class UserTransactions(TimeStampedModel):
    TRANSACTION_TYPE = (
        ('deposit', 'deposit'),
        ('withdrawal', 'withdrawal')
    )
    TRANSACTION_STATUS = (
        ('approved', 'approved'),
        ('pending', 'pending'),
        ('declined', 'declined'),
    )
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user_transaction')
    amount = models.FloatField()
    wallet_type = models.ForeignKey(PaymentMethod, on_delete=models.DO_NOTHING, related_name='payment_type')
    t_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE, default='')
    t_status = models.CharField(max_length=10, choices=TRANSACTION_STATUS, default='pending')
    
    
class WithdrawalGasFee(models.Model):
    select_transaction = models.ForeignKey(UserTransactions, on_delete=models.DO_NOTHING, related_name='withdrawal_fee')
    withdrawal_charges = models.FloatField(default=0.1018)
    paid = models.BooleanField(default=False)