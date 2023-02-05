from django import forms
from accounts.models import *
from marketplace.models import Category, CreateNftModel
from .models import PaymentMethod

class CreateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username',
                  'first_name',
                  'last_name', 
                  'email', 
                  'password', 
                  'balance', 
                  'is_active', 
                  'is_user',
                  'is_admin', 
                  'profile_pic', 
                  'cover_photo']
        

class CreateNftForm(forms.ModelForm):
    class Meta:
        model = CreateNftModel
        fields = ['name',
                  'creator',
                  'description',
                  'item_price',
                  'size',
                  'properties',
                  'upload_nft',
                  'royalties',
                  'collection',
                  'nft_type',
                  'bid',
                  'purchased_by',
                  'status',
                  'list_for_sale',
                  'minted',
                  'gas_fee',
                  
                ]
        
        
class AddPaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = ['coin_name',
                  'coin_address',
                  'coin_qr_code',
                  'coin_network',
                  'wallet_type',
                  'enable',
                 ]
        

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'name',
        ]