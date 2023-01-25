from django.shortcuts import render
from django.views.generic import TemplateView
from accounts.models import MoreDetails, User
from marketplace.models import CreateNftModel, NftCollection

from users.forms import EditMoreDetailsForm, EditProfileForm, UploadNftForm
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.shortcuts import HttpResponseRedirect, get_object_or_404, redirect, render
from django.contrib.auth.hashers import check_password
# Create your views here.

class UsersDashboard(TemplateView):
    template_name = 'users/index.html'
    def get(self, request):
        created = CreateNftModel.objects.filter(creator=self.request.user.uuid).order_by('-created')
        owned = CreateNftModel.objects.filter(creator=self.request.user.uuid, purchased_by=self.request.user.uuid).order_by('-created')
        sales = CreateNftModel.objects.filter(creator=self.request.user.uuid, list_for_sale=True).order_by('-created')
        context = {
            'created':created,
            'owned':owned,
            'sales':sales,
        }
        return render(request, self.template_name, context)
    
    
class EditProfile(TemplateView):
    ##Update for Profile Picture and cover image
    template_name = 'users/edit-profile.html'
    def get(self, request):
        # user = get_user_model(User)
        user = get_object_or_404(User, uuid=self.request.user.uuid)
        more_details = get_object_or_404(MoreDetails, user_details=user)
        types = more_details.Genders.choices
        form = EditProfileForm(instance=user)
        moredetailsform = EditMoreDetailsForm(instance=more_details)
        return render(request, self.template_name, {'form':form, 'moredetailsform':moredetailsform, 'user':user, 'more_details':more_details, 'types':types})
    
    
    def post(self, request):
        user = get_object_or_404(User, uuid=self.request.user.uuid)
        form = EditProfileForm(request.POST or None, request.FILES or None, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Updated')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'Error, Failed to update profile')
            return redirect(request.META.get('HTTP_REFERER'))
        
    
class UpdateDetails(TemplateView):
    def post(self, request):
        ## user model
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        
        #moredetails model
        bio = request.POST['bio']
        work_role = request.POST['work_role']
        gender = request.POST['gender']
        phone_number = request.POST['phone_number']
        location = request.POST['location']
        address = request.POST['address']
        
        u_user = get_object_or_404(User, uuid=self.request.user.uuid)
        u_details = MoreDetails.objects.get(user_details=self.request.user)
       
        if u_user and u_details:
            u_user.first_name = first_name
            u_user.last_name = last_name
            u_user.save()
            
            #More details
            u_details.bio = bio
            u_details.work_role = work_role
            u_details.gender = gender
            u_details.phone_number = phone_number
            u_details.location = location
            u_details.address = address
            u_details.save()
            messages.success(request, 'Profile Updated')
            return redirect('edit-profile')
        else:
            messages.error(request, 'Profile failed to update')
            return redirect('edit-profile')
        

class ChangePassword(TemplateView):
    template_name = 'users/edit-profile.html'
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        user = get_object_or_404(User, uuid=self.request.user.uuid)
        last_password = user.password
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        match_check = check_password(last_password, old_password)
        if user is not None:
            if user and check_password(old_password, user.password):
                if new_password == confirm_password:
                    user.get_user_p = new_password
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, 'Password changed. Login again')
                    return redirect('login')
                else:
                    messages.error(request, 'Password does not match')
                    return redirect('edit-profile')
            else:
                messages.error(request, 'Incorrect old password')
                return redirect('edit-profile')
        else:
            messages.error(request, 'User does not exist')
            return redirect('login')
        
        

"""Create NFT View"""
class UploadNft(TemplateView):
    template_name = 'users/nft/upload.html'
    def get(self, request):
        collections = NftCollection.objects.filter(user_collection=self.request.user)
        form = UploadNftForm()
        context = {'collections':collections, 'form':form}
        return render(request, self.template_name, context)
    
    def post(self, request):
        upload_nft = request.FILES.get('upload_nft')
        name = request.POST.get('name')
        description = request.POST.get('description')
        item_price = request.POST.get('item_price')
        size = request.POST.get('size')
        properties = request.POST.get('properties')
        nft_type = request.POST.get('nft_type')
        collection = request.POST.get('collection')
        royalties = request.POST.get('royalties')
        list_for_sale = request.POST.get('list_for_sale')
        bid = request.POST.get('bid')

        if name:
            if nft_type:
                if item_price:
                    CreateNftModel.objects.create(upload_nft=upload_nft, 
                                                  name=name, 
                                                  description=description, 
                                                  item_price=item_price, 
                                                  size=size, 
                                                  properties=properties, 
                                                  nft_type=nft_type, 
                                                  collection_id=collection, 
                                                  royalties=royalties,
                                                  list_for_sale=list_for_sale,
                                                  bid=bid,
                                                  creator=self.request.user).save()
                    messages.success(request, 'Art successfully uploaded')
                    return redirect('users')
                else:
                    messages.error(request, 'Price must be set')
                    return redirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, 'NFT Type must be set')
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'Product Name cannot be left blank')
            return redirect(request.META.get('HTTP_REFERER'))
                    
                    
class UploadNftDetail(TemplateView):
    template_name = 'users/nft/details.html'
    def get(self, request, slug, collection):
        # get_collection = get_object_or_404(NftCollection, name=collection)
        nft = get_object_or_404(CreateNftModel, slug=slug)
        return render(request, self.template_name, {'nft':nft})