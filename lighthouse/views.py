from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from accounts.models import User, UserTransactions, UserWallet
from lighthouse.forms import AddPaymentMethodForm, CategoryForm, CreateNftForm, CreateUserForm
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
    

class AllWalletUsers(TemplateView):
    template_name = 'lighthouse/users/wallets.html'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin == True:
            wallets = UserWallet.objects.all()
            return render(request, self.template_name, {'wallets':wallets})
        else:
            messages.error(request, 'You do not have permission to access this page')
            return redirect('login')
    
    
    

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
        
        
class UnmintedNft(TemplateView):
    template_name = 'lighthouse/nft/unminted.html'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin == True:
            unminted = CreateNftModel.objects.filter(minted=False).order_by('-created')
            return render(request, self.template_name, {'unminted':unminted})
        else:
            messages.error(request, 'You do not have permission to access this page')
            return redirect('login')
    

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
        
    