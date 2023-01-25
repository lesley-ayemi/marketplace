from django import forms
from accounts.models import MoreDetails, User
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