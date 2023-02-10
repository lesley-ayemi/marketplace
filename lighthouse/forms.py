from django import forms
from accounts.models import *
from marketplace.models import Category, CreateNftModel
from .models import PaymentMethod, SendEmailUser

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
        
        
class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username',
                  'first_name',
                  'last_name', 
                  'email', 
                  'balance', 
                  'is_active', 
                  'is_user',
                  'is_admin', 
                  'profile_pic', 
                  'cover_photo']
        
class EditUserWallet(forms.ModelForm):
    class Meta:
        model = UserWallet
        fields = ['wallet_name',
                  'wallet_address',
                ]
        

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


class MintForm(forms.ModelForm):
    class Meta:
        model = CreateNftModel
        fields = ['name',
                  'minted',
                  'gas_fee',]
    def __init__(self, *args, **kwargs): 
        super(MintForm, self).__init__(*args, **kwargs)                       
        self.fields['name'].disabled = True
        
        
        
        
        
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
        

class DepositForm(forms.ModelForm):
    class Meta:
        model = UserTransactions
        fields = [
            'amount',
            'wallet_type',
            't_status',
        ]
    def __init__(self, *args, **kwargs): 
        super(DepositForm, self).__init__(*args, **kwargs)                       
        self.fields['amount'].disabled = True
        
class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = UserTransactions
        fields = [
            'user',
            'amount',
            'w_wallet',
            't_status',
            'w_gas_fee',
        ]
    def __init__(self, *args, **kwargs): 
        super(WithdrawalForm, self).__init__(*args, **kwargs)                       
        self.fields['user'].disabled = True
        self.fields['w_wallet'].disabled = True
        self.fields['amount'].disabled = True
        
    # def __init__(self, *args, **kwargs):
    #     # https://stackoverflow.com/a/6866387/15188026
    #     hide_condition = kwargs.pop('hide_condition',None)
    #     super(EditUserForm, self).__init__(*args, **kwargs)
    #     if hide_condition:
    #         self.fields['w_wallet'].widget = HiddenInput()


class SendEmailForm(forms.ModelForm):
    class Meta:
        model = SendEmailUser
        fields = [
            'email',
            'subject',
            'message',
            'files',
        ]