import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from mutual.models import TimeStampedModel
from cloudinary.models import CloudinaryField
from lighthouse.models import PaymentMethod
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    balance = models.FloatField(null=True, blank=True, default=0)
    is_admin = models.BooleanField(default=False)
    is_user = models.BooleanField(default=True)
    get_user_p = models.CharField(blank=True, null=True, max_length=255)
    profile_pic = CloudinaryField('image', folder = "/profile-pic/", default='https://res.cloudinary.com/dbbfeegje/image/upload/v1673299668/cld-sample.jpg')
    cover_photo = CloudinaryField('image', folder = "/cover-photo/", default="https://res.cloudinary.com/dbbfeegje/image/upload/v1673299668/cld-sample-2.jpg")
    

class MoreDetails(TimeStampedModel):
    class Genders(models.TextChoices):
        Male = 'male'
        Woman = 'woman'
        Transgender = 'transgender'
        Non_binary = 'non-binary/non-conforming'
        prefer_not_to_respond = 'Prefer not to respond'
    user_details = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name='user_details', null=True, blank=True)
    bio = models.TextField(blank=True, default='')
    work_role = models.CharField(max_length=100, default='')
    gender = models.CharField(max_length=100, choices=Genders.choices, default='')
    phone_number = models.CharField(max_length=100, default='')
    location = models.CharField(max_length=100, default='')
    address = models.CharField(max_length=255, default='')
    
    @receiver(post_save, sender=User)
    def create_more_details(sender, instance, created, **kwargs):
        if created:
            MoreDetails.objects.create(
                user_details=instance
            )
    
    # post_save.connect(create_more_details, sender=User)
    
class UserWallet(TimeStampedModel):
    user_wallet = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='user_wallet')
    wallet_name = models.CharField(max_length=200)
    wallet_address = models.TextField()
    
    
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
    wallet_type = models.ForeignKey(PaymentMethod, on_delete=models.DO_NOTHING, related_name='payment_type', null=True, blank=True)
    t_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE, default='')
    t_status = models.CharField(max_length=10, choices=TRANSACTION_STATUS, default='pending')
    w_wallet = models.ForeignKey(UserWallet, on_delete=models.SET_NULL, null=True, blank=True, related_name='withdrawal_wallet')
    upload_proof = CloudinaryField('image', folder = "/deposits/", blank=True, null=True)
    
    def __str__(self):
        return str(self.user)
    
    
class WithdrawalGasFee(TimeStampedModel):
    select_transaction = models.ForeignKey(UserTransactions, on_delete=models.DO_NOTHING, related_name='withdrawal_fee')
    withdrawal_charges = models.FloatField(default=0.1018)
    paid = models.BooleanField(default=False)