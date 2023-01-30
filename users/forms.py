from django import forms
from accounts.models import MoreDetails, User, UserWallet
from marketplace.models import *

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','profile_pic', 'cover_photo']
        

class EditMoreDetailsForm(forms.ModelForm):
    class Meta:
        model = MoreDetails
        fields = ['bio', 'work_role', 'gender', 'phone_number', 'location', 'address']
        # exclude = ['user_details']
        

class UploadNftForm(forms.ModelForm):
    class Meta:
        model = CreateNftModel
        fields = ['upload_nft', 'name', 'item_price', 'description', 'size', 'properties', 'nft_type', 'royalties', 'collection', 'bid', 'list_for_sale']
        

class EditNftForm(forms.ModelForm):
    # def __init__(self, user, *args, **kwargs):
    #     super(EditNftForm, self).__init__(*args, **kwargs)
    #     self.fields['collection'] = forms.ChoiceField(
    #         choices=[(o.id, str(o)) for o in NftCollection.objects.filter(user_collection= user)]
    #     )
    class Meta:
        model = CreateNftModel
        fields = ['upload_nft', 'name', 'item_price', 'description', 'size', 'properties', 'nft_type', 'royalties', 'collection', 'bid', 'list_for_sale']
        
        
        
class EditCollectionForm(forms.ModelForm):
    class Meta:
        model = NftCollection
        fields = ['logo_image', 'banner_image', 'featured_image', 'name', 'custom_url', 'description', 'category', 'creator_earning', 'payout_address', 'blockchain', 'sensitive_content']
        
        

class UserAddWalletForm(forms.ModelForm):
    class Meta:
        model = UserWallet
        fields = ['wallet_name', 'wallet_address']