from django.shortcuts import render
from django.views.generic import TemplateView
from accounts.models import MoreDetails, User, UserTransactions, UserWallet
from lighthouse.models import PaymentMethod
from marketplace.models import BidNft, Category, CreateNftModel, NftCollection

from users.forms import EditCollectionForm, EditMoreDetailsForm, EditNftForm, EditProfileForm, UploadNftForm, UserAddWalletForm
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.shortcuts import HttpResponseRedirect, get_object_or_404, redirect, render
from django.contrib.auth.hashers import check_password
from django.db.models import Count
from django.db.models import Q
from django.db.models import Avg, Max, Min, Sum, Value as V
from django.db.models.functions import Coalesce
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

"""Dashboard"""
class UsersDashboard(LoginRequiredMixin, TemplateView):
    template_name = 'users/index.html'
    def get(self, request):
        created = CreateNftModel.objects.filter(creator=self.request.user.uuid).order_by('-created')
        owned = CreateNftModel.objects.filter(creator=self.request.user.uuid, purchased_by=self.request.user.uuid).order_by('-created')
        total_purchases = CreateNftModel.objects.filter(purchased_by=self.request.user.uuid).count()
        sales = CreateNftModel.objects.filter(creator=self.request.user.uuid, list_for_sale=True).order_by('-created')
        my_collections = NftCollection.objects.filter(user_collection=self.request.user.uuid)
        # TODO: fix count for collection items 
        collection_items = CreateNftModel.objects.filter(Q(collection=my_collections) and Q(creator_id=self.request.user.uuid)).count()
        # collection_items = CreateNftModel.objects.filter(collection_id__user_collection_id=self.request.user.uuid).count()
        unminted = CreateNftModel.objects.filter(Q(creator=request.user), Q(minted=False)).aggregate(Sum('gas_fee', default=0))
        payments = PaymentMethod.objects.filter(wallet_type='minting', enable=True).order_by('-created')
        context = {
            'created':created,
            'owned':owned,
            'sales':sales,
            'my_collections':my_collections,
            'unminted':unminted,
            'payments':payments,
            'total_purchases':total_purchases,
        }
        return render(request, self.template_name, context)
    

"""Profile Page"""
class EditProfile(LoginRequiredMixin, TemplateView):
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
        
"""More on Profile""" 
class UpdateDetails(LoginRequiredMixin, TemplateView):
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
        
"""Change Password"""
class ChangePassword(LoginRequiredMixin, TemplateView):
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
        
        

"""Create NFT"""
class UploadNft(LoginRequiredMixin, TemplateView):
    template_name = 'users/nft/upload.html'
    def get(self, request):
        collections = NftCollection.objects.filter(user_collection=self.request.user)
        form = UploadNftForm()
        context = {'collections':collections, 'form':form}
        return render(request, self.template_name, context)
    @transaction.atomic
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
        
"""Edit NFT"""
class EditNft(LoginRequiredMixin, TemplateView):
    template_name = 'users/nft/edit-nft.html'
    def get(self, request, slug):
        nft = get_object_or_404(CreateNftModel, slug=slug)
        collections = NftCollection.objects.filter(user_collection=self.request.user)
        types = nft.NFT_TYPE.choices
        form = EditNftForm(instance=nft)
       
        context = {'nft':nft, 'collections':collections, 'types':types, 'form':form}
        return render(request, self.template_name, context)
    
    def post(self, request, slug):
        # TODO: come back and fix sorting collections by user 
        nft = get_object_or_404(CreateNftModel, slug=slug)
        # user = get_object_or_404(User, )
        form = EditNftForm(request.POST or None, request.FILES or None, instance=nft)
        if form.is_valid():
            form.save()
            # user.creator = self.request.user
            # user.save()
            messages.success(request, 'Updated form')
            return redirect('users')
        else:
            messages.error(request, 'Error, unable to update')
            return redirect(request.META.get('HTTP_REFERER'))
        
        # upload_nft = request.FILES.get('upload_nft')
        # name = request.POST.get('name')
        # description = request.POST.get('description')
        # item_price = request.POST.get('item_price')
        # size = request.POST.get('size')
        # properties = request.POST.get('properties')
        # nft_type = request.POST.get('nft_type')
        # collection = request.POST.get('collection')
        # royalties = request.POST.get('royalties')
        # list_for_sale = request.POST.get('list_for_sale')
        # bid = request.POST.get('bid')

        # update_nft = get_object_or_404(CreateNftModel, slug=slug)
        
        # if name:
        #     if nft_type:
        #         if item_price:
        #             update_nft.upload_nft = upload_nft
        #             update_nft.name = name
        #             update_nft.description = description
        #             update_nft.item_price = item_price
        #             update_nft.size = size
        #             update_nft.properties = properties
        #             update_nft.nft_type = nft_type
        #             update_nft.collection_id = collection
        #             update_nft.royalties = royalties
        #             update_nft.list_for_sale = list_for_sale
        #             update_nft.bid = bid
        #             update_nft.save()
        #             messages.success(request, 'Update Sucessfully')
        #             return redirect('users')
        #         else:
        #             messages.error(request, 'Price must be set')
        #             return redirect(request.META.get('HTTP_REFERER'))
        #     else:
        #         messages.error(request, 'NFT Type must be set')
        #         return redirect(request.META.get('HTTP_REFERER'))
        # else:
        #     messages.error(request, 'Product Name cannot be left blank')
        #     return redirect(request.META.get('HTTP_REFERER'))
        
        
"""Delete NFT"""
class DeleteNft(LoginRequiredMixin, TemplateView):
    template_name = 'users/nft/delete-nft.html'
    def get(self, request, slug):
        nft = get_object_or_404(CreateNftModel, slug=slug)
        return render(request, self.template_name, {'nft':nft})
    
    def post(self, request, slug):
        nft = get_object_or_404(CreateNftModel, slug=slug)
        if nft:
            nft.delete()
            messages.success(request, 'NFT removed successfully')
            return redirect('users')
        else:
            messages.error(request, 'NFT does not exists')
            return redirect('users')
                    
                    
"""Details Page NFT"""
class UploadNftDetail(LoginRequiredMixin, TemplateView):
    template_name = 'users/nft/details.html'
    def get(self, request, slug):
        # get_collection = get_object_or_404(NftCollection, name=collection)
        nft = get_object_or_404(CreateNftModel, slug=slug)
        payments = PaymentMethod.objects.filter(wallet_type='minting', enable=True).order_by('-created')
        return render(request, self.template_name, {'nft':nft, 'payments':payments})
    
    def post(self, request, *args, **kwargs):
        nft = get_object_or_404(CreateNftModel, slug=kwargs.get('slug'))
        if nft:
            nft.mint_proof = request.FILES.get('mint_proof')
            nft.save()
            messages.success(request, 'NFT details updated successfully')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'NFT does not exists')
            return redirect(request.META.get('HTTP_REFERER'))
    
    

"""Collections"""
class CreateCollection(LoginRequiredMixin, TemplateView):
    template_name = 'users/nft/create-collection.html'
    def get(self, request):
        categories = Category.objects.all()
        context = {
            'categories':categories,
        }
        return render(request, self.template_name, context)
    
    
    def post(self, request):
        logo_image = request.FILES.get('logo_image')
        banner_image = request.FILES.get('banner_image')
        featured_image = request.FILES.get('featured_image')
        name = request.POST.get('name')
        custom_url = request.POST.get('custom_url')
        category = request.POST.get('category')
        description = request.POST.get('description')
        creator_earning = request.POST.get('creator_earning')
        payout_address = request.POST.get('payout_address')
        blockchain = request.POST.get('blockchain')
        sensitive_content = request.POST['sensitive_content'] == 'true'
        if name:
            if category:
                if description:
                    if payout_address:
                        NftCollection.objects.create(logo_image=logo_image,
                                                     banner_image=banner_image,
                                                     featured_image=featured_image,
                                                     name=name,
                                                     custom_url=custom_url,
                                                     category_id=category,
                                                     description=description,
                                                     creator_earning=creator_earning,
                                                     payout_address=payout_address,
                                                     blockchain=blockchain,
                                                     sensitive_content=sensitive_content,
                                                     user_collection_id=self.request.user.uuid
                                                     ).save()
                        messages.success(request, 'Collection Created')
                        return redirect('users')
                    else:
                        messages.error(request, 'Payout address is needed')
                        return redirect(request.META.get('HTTP_REFERER'))
                else:
                    messages.error(request, 'Description is needed')
                    return redirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, 'Select a category')
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'Name field is required')
            return redirect(request.META.get('HTTP_REFERER'))
        
        
"""Edit Collections"""

class EditCollection(LoginRequiredMixin, TemplateView):
    template_name = 'users/nft/edit-collection.html'
    def get(self, request, slug):
        collection = get_object_or_404(NftCollection, slug=slug)
        form = EditCollectionForm(instance=collection)
        return render(request, self.template_name, {'collection':collection, 'form':form})
    
    def post(self, request, slug):
        collection = get_object_or_404(NftCollection, slug=slug)
        form = EditCollectionForm(request.POST or None, request.FILES or None, instance=collection)
        if form.is_valid():
            form.save()
            messages.success(request, 'Collection updated')
            return redirect('users')
        else:
            messages.error(request, 'Collection failed to update')
            return redirect(request.META.get('HTTP_REFERER'))
        
        
"""Delete Collection"""
class DeleteCollection(LoginRequiredMixin, TemplateView):
    template_name = 'users/nft/delete-collection.html'
    def get(self, request, slug):
        collection = get_object_or_404(NftCollection, slug=slug)
        return render(request, self.template_name, {'collection':collection})
    
    def post(self, request, slug):
        nfcollection = get_object_or_404(CreateNftModel, slug=slug)
        if nfcollection:
            nfcollection.delete()
            messages.success(request, 'Collection removed successfully')
            return redirect('users')
        else:
            messages.error(request, 'collection does not exists')
            return redirect('users')
        
        
"""View Collection"""
class ViewCollection(LoginRequiredMixin, TemplateView):
    template_name = 'users/nft/view-collection.html'
    def get(self, request, slug):
        collection = get_object_or_404(NftCollection, slug=slug)
        items = CreateNftModel.objects.filter(collection=collection)
        return render(request, self.template_name, {'collection':collection, 'items':items})
    
    
"""Wallet View"""

class AddWallet(LoginRequiredMixin, TemplateView):
    template_name = 'users/wallets/add.html'
    def get(self, request):
        form = UserAddWalletForm()
        all_wallets = UserWallet.objects.filter(user_wallet=self.request.user)
        return render(request, self.template_name, {'form':form, 'all_wallets':all_wallets})
    
    def post(self, request):
        form = UserAddWalletForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_wallet = self.request.user
            user.save()
            messages.success(request, 'Wallet Added')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'Failed to add wallet, Try again..')
            return redirect(request.META.get('HTTP_REFERER'))
        
        
class DeleteWallet(LoginRequiredMixin, TemplateView):
    def get(self, request, id):
        wallet = get_object_or_404(UserWallet, id=id)
        return render(request, 'users/wallets/delete.html', {'wallet':wallet})
    
    def post(self, request, id):
        wallet = get_object_or_404(UserWallet, id=id)
        if wallet:
            wallet.delete()
            messages.success(request, 'Wallet deleted')
            return redirect('add-wallet')
        else:
            messages.error(request, 'Wallet does not exists')
            return redirect('add-wallet')


class FundAccount(LoginRequiredMixin, TemplateView):
    template_name = 'users/deposits/add.html'
    def get(self, request):
        wallets = PaymentMethod.objects.filter(wallet_type='deposit', enable=True)
        transactions = UserTransactions.objects.filter(t_type='deposit', user_id=self.request.user.uuid)
        return render(request, self.template_name, {'wallets':wallets, 'transactions':transactions})
    
    
class FundAccountDetail(LoginRequiredMixin, TemplateView):
    template_name = 'users/deposits/add-details.html'
    def get(self, request, id):
        wallet = get_object_or_404(PaymentMethod, id=id)
        return render(request, self.template_name, {'wallet':wallet})
    
    def post(self, request, id):
        amount = request.POST['amount']
        upload_proof = request.FILES.get('upload_proof')
        wallet = get_object_or_404(PaymentMethod, id=id)
        user = get_object_or_404(User, uuid=self.request.user.uuid)
        
        if amount:
            if float(amount) > 0:
                if user:
                    UserTransactions.objects.create(
                        user=user,
                        amount=float(amount),
                        wallet_type=wallet,
                        t_type='deposit',
                        t_status='pending',
                        upload_proof=upload_proof,
                    ).save()
                    messages.success(request, 'Deposit successful and under review')
                    return redirect(request.META.get('HTTP_REFERER'))
                else:
                    messages.error(request, 'error,failed to authenticate user')
                    return redirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, '0 cannot be deposited')
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'amount cannot left empty')
            return redirect(request.META.get('HTTP_REFERER'))
        
        
class WithdrawAccount(LoginRequiredMixin, TemplateView):
    template_name = 'users/withdrawals/request.html'
    def get(self, request):
        u_wallets = UserWallet.objects.filter(user_wallet_id=self.request.user.uuid)
        transactions = UserTransactions.objects.filter(t_type='withdrawal', user_id=self.request.user.uuid)
        return render(request, self.template_name, {'transactions':transactions, 'u_wallets':u_wallets})
    
    def post(self, request):
        amount = request.POST['amount']
        wallet_name = request.POST.get('wallet_name')
        my_wallet = get_object_or_404(UserWallet, id=wallet_name)
        # my_wallet = UserWallet.objects.filter(id=wallet_name)
        user = get_object_or_404(User, uuid=self.request.user.uuid)
        
        if my_wallet:
            if amount:
                if float(amount) <= user.balance:
                    if float(amount) != 0:
                        UserTransactions.objects.create(
                            user=user,
                            amount=float(amount),
                            t_type='withdrawal',
                            t_status='pending',
                            w_wallet=my_wallet,
                        ).save()
                        messages.success(request, 'Withdrawal in queue and pending')
                        return redirect(request.META.get('HTTP_REFERER'))
                    else:
                        messages.error(request, 'Zero cannot be withdrawn')
                        return redirect(request.META.get('HTTP_REFERER'))
                else:
                    messages.error(request, 'You amount cannot be greater than your balance')
                    return redirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, 'Amount cannot be left empty')
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'select wallet for withdrawal')
            return redirect(request.META.get('HTTP_REFERER'))