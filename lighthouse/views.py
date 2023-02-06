from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from accounts.models import User, UserTransactions, UserWallet
from lighthouse.forms import AddPaymentMethodForm, CategoryForm, CreateNftForm, CreateUserForm, EditUserForm, EditUserWallet, MintForm
from django.contrib import messages
from lighthouse.models import PaymentMethod

from marketplace.models import Category, CreateNftModel

# Create your views here.
class LighthouseDashboard(TemplateView):
    template_name = 'lighthouse/dashboard.html'
    def get(self, request, *args):
        if request.user.is_authenticated and request.user.is_admin == True:
            return render(request, self.template_name, *args)
        else:
            messages.error(request, 'You do not have permission to access this page')
            return redirect('login')
    
    
class Categories(TemplateView):
    template_name = 'lighthouse/category/all.html'
    def get(self, request, *args):
        if request.user.is_authenticated and request.user.is_admin == True:
            categories = Category.objects.all()
            form = CategoryForm()
            return render(request, self.template_name, {'categories': categories, 'form': form})
        else:
            messages.error(request, 'You do not have permission to access this page')
            return redirect('login')
    
    def post(self, request):
        form = CategoryForm(request.POST or None)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            messages.success(request, 'Category created successfully')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'Category creation failed')
            return redirect(request.META.get('HTTP_REFERER'))
        
        
class EditCategory(TemplateView):
    template_name = 'lighthouse/category/edit.html'
    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        if request.user.is_authenticated and request.user.is_admin == True:
            form = CategoryForm(instance=category)
            return render(request, self.template_name, {'form': form, 'category':category})
        else:
            messages.error(request, 'You do not have permission to access this page')
            return redirect('login')
    
    def post(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        if request.user.is_authenticated and request.user.is_admin == True:
            form = CategoryForm(request.POST or None, instance=category)
            if form.is_valid():
                form.save()
                messages.success(request, 'Category updated successfully')
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, 'Category update failed')
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'You do not have permission to access this page')
            return redirect('login')
    
class CreateUser(TemplateView):
    template_name = 'lighthouse/users/create.html'
    def get(self, request):
        if request.user.is_authenticated and request.user.is_admin == True:
            form = CreateUserForm()
            return render(request, self.template_name, {'form': form})
        else:
            messages.error(request, 'You do not have permission to access this page')
            return redirect('login')
    
    def post(self, request):
        form = CreateUserForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.get_user_p = password
            user.set_password(password)
            user.save()
            messages.success(request, 'User created successfully')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'User creation failed')
            return redirect(request.META.get('HTTP_REFERER'))
    
class AllUsers(TemplateView):
    template_name = 'lighthouse/users/all.html'
    def get(self, request):
        if request.user.is_authenticated and request.user.is_admin == True:
            all_users = User.objects.filter(is_user=True).order_by('-date_joined')
            return render(request, self.template_name, {'all_users': all_users})
        else:
            messages.error(request, 'You do not have permission to access this page')
            return redirect('login')
    
    
class EditUser(TemplateView):
    template_name = 'lighthouse/users/edit.html'
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        form = EditUserForm(instance=user)
        # form_wallet = EditUserWallet(instance=user)
        return render(request, self.template_name, {'form': form, 'user': user})

    def post(self, request, username):
        user = get_object_or_404(User, username=username)
        form = EditUserForm(request.POST or None, request.FILES or None, instance=user)
        # form_wallet = EditUserWallet(request.POST or None, request.FILES or None, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            # form_wallet.save()
            messages.success(request, 'User updated successfully')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'User update failed')
            return redirect(request.META.get('HTTP_REFERER'))
        
class DeleteUser(TemplateView):
    template_name = 'lighthouse/users/delete.html'
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        return render(request, self.template_name, {'user': user})
    
    def post(self, request, username):
        user = get_object_or_404(User, username=username)
        user.delete()
        messages.success(request, 'User deleted successfully')
        return redirect('all-users')

class AllWalletUsers(TemplateView):
    template_name = 'lighthouse/users/wallets.html'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin == True:
            wallets = UserWallet.objects.all()
            return render(request, self.template_name, {'wallets':wallets})
        else:
            messages.error(request, 'You do not have permission to access this page')
            return redirect('login')
        
class UserWallet(TemplateView):
    template_name = 'lighthouse/users/user-wallet.html'
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        wallets = UserWallet.objects.filter(user=user)
        return render(request, self.template_name, {'wallets':wallets})
    
    def post(self, request, username):
        pass

class AllNft(TemplateView):
    template_name = 'lighthouse/nft/all.html'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin == True:
            nfts = CreateNftModel.objects.all().order_by('name')
            return render(request, self.template_name, {'nfts':nfts})
        else:
            messages.error(request, 'You do not have permission to access this page')
            return redirect('login')
    
    
class CreateNft(TemplateView):
    template_name = 'lighthouse/nft/create-nft.html'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin == True:
            form = CreateNftForm()
            return render(request, self.template_name, {'form':form})
        else:
            messages.error(request, 'You do not have permission to access this page')
            return redirect('login')
    
    def post(self, request, *args, **kwargs):
        form = CreateNftForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'NFT created successfully')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'NFT not created successfully')
            return redirect(request.META.get('HTTP_REFERER'))
        
class AdminEditNft(TemplateView):
    template_name = 'lighthouse/nft/edit-nft.html'
    def get(self, request, slug):
        nft = get_object_or_404(CreateNftModel, slug=slug)
        form = CreateNftForm(instance=nft)
        return render(request, self.template_name, {'form':form, 'nft':nft})
    
    def post(self, request, slug):
        nft = get_object_or_404(CreateNftModel, slug=slug)
        form = CreateNftForm(request.POST or None, request.FILES or None, instance=nft)
        if form.is_valid():
            form.save()
            messages.success(request, 'NFT updated successfully')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'NFT not updated successfully')
            return redirect(request.META.get('HTTP_REFERER'))
        
class AdminDeleteNft(TemplateView):
    template_name = 'lighthouse/nft/delete-nft.html'
    def get(self, request, slug):
        nft = get_object_or_404(CreateNftModel, slug=slug)
        return render(request, self.template_name, {'nft':nft})
    
    def post(self, request, slug):
        nft = get_object_or_404(CreateNftModel, slug=slug)
        nft.delete()
        messages.success(request, 'NFT deleted successfully')
        return redirect('all-nfts')
        
        
class UnmintedNft(TemplateView):
    template_name = 'lighthouse/nft/unminted.html'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin == True:
            unminted = CreateNftModel.objects.filter(minted=False).order_by('-created')
            return render(request, self.template_name, {'unminted':unminted})
        else:
            messages.error(request, 'You do not have permission to access this page')
            return redirect('login')
        
class EditUnmintedNft(TemplateView):
    template_name = 'lighthouse/nft/edit-unminted.html'
    def get(self, request, slug):
        unminted = get_object_or_404(CreateNftModel, slug=slug)
        form = MintForm(instance=unminted)
        return render(request, self.template_name, {'form':form, 'unminted':unminted})
    
    def post(self, request, slug):
        unminted = get_object_or_404(CreateNftModel, slug=slug)
        form = MintForm(request.POST, instance=unminted)
        if form.is_valid():
            form.save()
            messages.success(request, 'NFT Updated successfully')
            return redirect('unminted-nfts')
        else:
            messages.error(request, 'NFT not updated successfully')
            return redirect('unminted-nfts')
    

class ApprovedDeposits(TemplateView):
    template_name = 'lighthouse/deposits/approved.html'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin == True:
            deposits = UserTransactions.objects.filter(t_type='deposit', t_status='approved').order_by('-created')
            return render(request, self.template_name, {'deposits':deposits})
        else:
            messages.error(request, 'You do not have permission to access this page')
            return redirect('login')
    
class PendingDeposits(TemplateView):
    template_name = 'lighthouse/deposits/pending.html'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin == True:
            deposits = UserTransactions.objects.filter(t_type='deposit', t_status='pending').order_by('-created')
            return render(request, self.template_name, {'deposits':deposits})
        else:
            messages.error(request, 'You do not have permission to access this page')
            return redirect('login')
class DeclinedDeposits(TemplateView):
    template_name = 'lighthouse/deposits/declined.html'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin == True:
            deposits = UserTransactions.objects.filter(t_type='deposit', t_status='declined').order_by('-created')
            return render(request, self.template_name, {'deposits':deposits})
        else:
            messages.error(request, 'You do not have permission to access this page')
            return redirect('login')
    
    
class ApprovedWithdrawals(TemplateView):
    template_name = 'lighthouse/withdrawals/approved.html'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin == True:
            withdrawals = UserTransactions.objects.filter(t_type='withdrawal', t_status='approved').order_by('-created')
            return render(request, self.template_name, {'withdrawals':withdrawals})
        else:
            messages.error(request, 'You do not have permission to access this page')
            return redirect('login')
    
    
class PendingWithdrawals(TemplateView):
    template_name = 'lighthouse/withdrawals/pending.html'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin == True:
            withdrawals = UserTransactions.objects.filter(t_type='withdrawal', t_status='pending').order_by('-created')
            return render(request, self.template_name, {'withdrawals':withdrawals})
        else:
            messages.error(request, 'You do not have permission to access this page')
            return redirect('login')
    
class DeclinedWithdrawals(TemplateView):
    template_name = 'lighthouse/withdrawals/declined.html'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin == True:
            withdrawals = UserTransactions.objects.filter(t_type='withdrawal', t_status='declined').order_by('-created')
            return render(request, self.template_name, {'withdrawals':withdrawals})
        else:
            messages.error(request, 'You do not have permission to access this page')
            return redirect('login')
    
    
    
    
class AddPaymentMethod(TemplateView):
    template_name = 'lighthouse/payment-methods/add.html'
    def get(self, request):
        if request.user.is_authenticated and request.user.is_admin == True:
            form = AddPaymentMethodForm()
            payments = PaymentMethod.objects.all().order_by('coin_name')
            return render(request, self.template_name, {'form':form, 'payments':payments})
        else:
            messages.error(request, 'You do not have permission to access this page')
            return redirect('login')
    
    def post(self, request):
        form = AddPaymentMethodForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payment method added successfully')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'Payment method not added successfully')
            return redirect(request.META.get('HTTP_REFERER'))
        
    