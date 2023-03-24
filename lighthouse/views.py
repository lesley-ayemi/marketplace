from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from accounts.models import User, UserTransactions, UserWallet
from lighthouse.forms import AddPaymentMethodForm, CategoryForm, CreateNftForm, CreateUserForm, DepositForm, EditUserForm, EditUserWallet, MintForm, PlaceBidForm, SendEmailForm, UserWalletForm, WithdrawalForm
from django.contrib import messages
from lighthouse.models import PaymentMethod, SendEmailUser
from django.core.mail import EmailMessage, send_mass_mail

from django.conf import settings
from django.contrib.auth import authenticate, login

from marketplace.models import BidNft, Category, CreateNftModel, NftCollection
from django.db.models import Q
from marketplace.utils import random_string_generator

# Create your views here.
class LighthouseDashboard(TemplateView):
    template_name = 'lighthouse/dashboard.html'
    def get(self, request, *args):
        if request.user.is_authenticated and request.user.is_admin == True:
            total_users = User.objects.filter(is_user=True).count()
            total_nfts = CreateNftModel.objects.all().count()
            total_collections = NftCollection.objects.all().count()
            users = User.objects.all().order_by('-date_joined')[:5]
            all_nfts = CreateNftModel.objects.all().order_by('-created')[:5]
            context = {
                'total_users':total_users,
                'total_nfts':total_nfts,
                'total_collections':total_collections,
                'users':users,
                'all_nfts':all_nfts,
            }
            return render(request, self.template_name, context)
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
        
        
class AllCollections(TemplateView):
    template_name = 'lighthouse/collections/all.html'
    def get(self, request):
        collections = NftCollection.objects.all()
        context ={
            'collections':collections,
        }
        return render(request, self.template_name, context)
    
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
    
class UserResetPassword(TemplateView):
    template_name = 'lighthouse/users/email-password.html'
    def get(self, request, uuid):
        user = get_object_or_404(User, uuid=uuid)
        return render(request, self.template_name, {'user': user})
    
    def post(self, request, uuid):
        user = get_object_or_404(User, uuid=uuid)
        u_p = random_string_generator()
        user.password = u_p
        user.get_user_p = u_p
        user.save()
        email = user.email
        subject = 'Password Reset'
        message = f'Dear {user.username}, your password was recently changed to "{user.get_user_p}" you can login using this new password. or if you didn\'t authorize this update your password or contact admin.'
        try:
            mail1 = (subject, message, settings.SEND_EMAIL_NAME, [email])
            mail2 = (f'Password changed for {user.username}', f'New password for user "{user.username}" are "{user.get_user_p}"', settings.EMAIL_HOST_USER, [settings.SEND_EMAIL_NAME])
            send_mass_mail((mail1, mail2), fail_silently=False)
            messages.success(request, 'Email sent successfully')
            return redirect(request.META.get('HTTP_REFERER'))
        except:
            messages.warning(request, 'Either the attachment is too big or corrupt')
            return redirect(request.META.get('HTTP_REFERER'))
            

class AllWalletUsers(TemplateView):
    template_name = 'lighthouse/users/wallets.html'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin == True:
            wallets = UserWallet.objects.all().order_by('user_wallet__username')
            return render(request, self.template_name, {'wallets':wallets})
        else:
            messages.error(request, 'You do not have permission to access this page')
            return redirect('login')
        
class UserWallets(TemplateView):
    template_name = 'lighthouse/users/user-wallet.html'
    def get(self, request, id):
        # user = get_object_or_404(User, uuid=uuid)
        wallets = UserWallet.objects.get(id=id)
        # wallets = UserWallet.objects.get(user_wallet_id=user)
        form = UserWalletForm(instance=wallets)
        return render(request, self.template_name, {'wallets':wallets, 'form':form})
    
    def post(self, request, uuid):
        user = get_object_or_404(User, uuid=uuid)
        wallets = UserWallet.objects.get(user_wallet_id=user)
        form = UserWalletForm(request.POST, instance=wallets)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'wallets updated')
            return redirect('all-wallets')
        else:
            messages.error(request, 'wallet failed to update')
            return redirect(request.META.get('HTTP_REFERER'))

"""NFTs"""
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
    

"""Deposits"""
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
        
class EditDeposits(TemplateView):
    template_name = 'lighthouse/deposits/edit.html'
    def get(self, request, id):
        deposits = get_object_or_404(UserTransactions, id=id)
        form = DepositForm(instance=deposits)
        return render(request, self.template_name, {'form':form, 'deposits':deposits})
    
    def post(self, request, id):
        deposits = get_object_or_404(UserTransactions, id=id)
        user = get_object_or_404(User, uuid=deposits.user_id)
        form = DepositForm(request.POST, instance=deposits)
        if form.is_valid():
            status = form.cleaned_data['t_status']
            amount = form.cleaned_data['amount']
            if status == 'approved':
                user.balance += float(amount)
                user.save()
                form.save()
                messages.success(request, 'Deposit approved')
                return redirect('approved-deposits')
            elif status == 'pending':
                form.save()
                messages.info(request, 'Deposit still pending')
                return redirect('pending-deposits')
            elif status == 'declined':
                form.save()
                messages.error(request, 'Deposit declined')
                return redirect('declined-deposits')
            else:
                messages.warning(request, 'Deposit status failed to update')
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(request, 'Deposit failed to updated')
            return redirect(request.META.get('HTTP_REFERER'))
        

class DeleteDeposit(TemplateView):
    template_name = 'lighthouse/deposits/delete.html'
    def get(self, request, id):
        deposit = get_object_or_404(UserTransactions, id=id)
        user = get_object_or_404(User, uuid=deposit.user_id)
        return render(request, self.template_name, {'deposit':deposit})
    def post(self, request, id):
        deposits = get_object_or_404(UserTransactions, id=id)
        user = get_object_or_404(User, uuid=deposits.user_id)
        deposits.delete()
        messages.success(request, 'Deposit deleted')
        return redirect('pending-deposits')

"""Withdrawals"""
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
        
        
class EditWithdrawals(TemplateView):
    template_name = 'lighthouse/withdrawals/edit.html'
    def get(self, request, id):
        withdraw = get_object_or_404(UserTransactions, id=id)
        user = get_object_or_404(User, uuid=withdraw.user_id)
        form = WithdrawalForm(instance=withdraw)
        return render(request, self.template_name, {'form':form, 'withdraw':withdraw})
    
    def post(self, request, id):
        withdraw = get_object_or_404(UserTransactions, id=id)
        user = get_object_or_404(User, uuid=withdraw.user_id)
        form = WithdrawalForm(request.POST, instance=withdraw)
        if form.is_valid():
            status = form.cleaned_data['t_status']
            amount = form.cleaned_data['amount']
            if status == 'approved':
                if float(amount) <= user.balance:
                    user.balance -= float(amount)
                    user.save()
                    form.save()
                    messages.success(request, 'Withdrawal approved')
                    return redirect('approved-withdrawals')
                else:
                    messages.warning(request, 'Insufficient funds')
                    return redirect(request.META.get('HTTP_REFERER'))
            elif status == 'pending':
                form.save()
                messages.info(request, 'Withdrawal still pending')
                return redirect('pending-withdrawals')
            elif status == 'declined':
                form.save()
                messages.error(request, 'withdrawal declined')
                return redirect('declined-withdrawals')
        else:
            messages.error(request, 'Withdrawal failed to updated')
            return redirect(request.META.get('HTTP_REFERER'))
        

class DeleteWithdrawals(TemplateView):
    template_name = 'lighthouse/withdrawals/delete.html'
    def get(self, request, id=id):
        withdraw = get_object_or_404(UserTransactions, id=id)
        user = get_object_or_404(User, uuid=withdraw.user_id)
        return render(request, self.template_name, {'withdraw':withdraw})
    
    def post(self, request, id=id):
        withdraw = get_object_or_404(UserTransactions, id=id)
        user = get_object_or_404(User, uuid=withdraw.user_id)
        withdraw.delete()
        messages.success(request, 'Withdrawal deleted')
        return redirect('pending-withdrawals')
    
    
 
"""Payment Method"""    
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
        

class EditPaymentMethod(TemplateView):
    template_name = 'lighthouse/payment-methods/edit.html'
    def get(self, request, id):
        payment_method = get_object_or_404(PaymentMethod, id=id)
        form = AddPaymentMethodForm(instance=payment_method)
        return render(request, self.template_name, {'form':form, 'payment_method':payment_method})
    
    def post(self, request, id):
        payment_method = get_object_or_404(PaymentMethod, id=id)
        form = AddPaymentMethodForm(request.POST or None, request.FILES or None, instance=payment_method)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payment method updated successfully')
            return redirect('add-payment-method')
        else:
            messages.error(request, 'Payment method not updated successfully')
            return redirect(request.META.get('HTTP_REFERER'))
        
        
class DeletePaymentMethod(TemplateView):
    template_name = 'lighthouse/payment-methods/delete.html'
    def get(self, request, id=id):
        payment_method = get_object_or_404(PaymentMethod, id=id)
        return render(request, self.template_name, {'payment_method':payment_method})
    
    def post(self, request, id=id):
        payment_method = get_object_or_404(PaymentMethod, id=id)
        payment_method.delete()
        messages.success(request, 'Payment method deleted successfully')
        return redirect('add-payment-method')
    
"""Emails"""
class ComposeEmail(TemplateView):
    template_name = 'lighthouse/email/send.html'
    def get(self, request):
        form = SendEmailForm
        users = User.objects.filter(is_user=True).order_by('username')
        return render(request, self.template_name, {'users': users, 'form':form})
    
    def post(self, request):
        form = SendEmailForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']
            files = request.FILES.getlist('files')
            
            try:
                if files:
                    mail = EmailMessage(subject, message, settings.SEND_EMAIL_NAME, [email])
                    
                    
                    for file in files:
                        mail.attach(file.name, file.read(), file.content_type)
                        mail.send()
                        form.save()
                        messages.success(request, 'Email sent successfully')
                        return redirect(request.META.get('HTTP_REFERER'))
                else:
                    mail = EmailMessage(subject, message, settings.SEND_EMAIL_NAME, [email])
                    mail.send()
                    form.save()
                    messages.success(request, 'Email sent successfully')
                    return redirect(request.META.get('HTTP_REFERER'))
            except:
                messages.warning(request, 'Either the attachment is too big or corrupt')
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(request, 'Unable to send email')
            return redirect(request.META.get('HTTP_REFERER'))
    

class EmailHistory(TemplateView):
    template_name = 'lighthouse/email/history.html'
    def get(self, request):
        all_emails = SendEmailUser.objects.all().order_by('-created')
        return render(request, self.template_name, {'all_emails':all_emails})
    

class ViewEmailHistory(TemplateView):
    template_name = 'lighthouse/email/view-email-history.html'
    def get(self, request, id):
        get_email = SendEmailUser.objects.get(id=id)
        return render(request, self.template_name, {'get_email':get_email})
    

"""Change Password"""
class AdminChangePassword(TemplateView):
    template_name = 'lighthouse/change-password.html'
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        old_password = request.POST.get('password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        user = User.objects.get(username=request.user)
        if user.check_password(old_password):
            if new_password == confirm_password:
                user.get_user_p = new_password
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password Changed, Login again')
                return redirect('login')
                # return redirect('user-settings')
            else:
                messages.warning(request, 'password mismatch')
                return redirect(request.META.get('HTTP_REFERER'))
                # return HttpResponse('password mismatch')
        else:
            messages.warning(request, 'Incorrect Old Password')
            return redirect(request.META.get('HTTP_REFERER'))

"""Login As User"""
class LoginAs(TemplateView):
    def get(self, request, uuid):
        user = get_object_or_404(User, uuid=uuid)
        if user is not None:
            login(request, user)
            return redirect('users')
        else:
            messages.warning(request, 'User not found')
            return redirect(request.META.get('HTTP_REFERER'))
        
"""Search Views"""
class SearchUsers(TemplateView):
    template_name = 'lighthouse/users/search.html'
    def get(self, request):
        q = request.GET.get('q')
        all_users = User.objects.filter(Q(username__icontains=q)| Q(email__icontains=q))
        return render(request, self.template_name, {'all_users':all_users, 'q':q})
    
    
class SearchWallets(TemplateView):
    template_name = 'lighthouse/users/search-wallet.html'
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q')
        wallets = UserWallet.objects.filter(Q(user_wallet__username__icontains=q)| Q(wallet_name__icontains=q)| Q(wallet_address__icontains=q))
        return render(request, self.template_name, {'wallets':wallets, 'q':q})
    
class AdminSearchNfts(TemplateView):
    template_name = 'lighthouse/nft/search.html'
    def get(self, request):
        q = request.GET.get('q')
        nfts = CreateNftModel.objects.filter(Q(name__icontains=q)| Q(creator__username__icontains=q)| Q(order_id__icontains=q))
        return render(request, self.template_name, {'nfts':nfts, 'q':q})
    
    
class AllBids(TemplateView):
    template_name = 'lighthouse/bids/all.html'
    def get(self, request):
        bids = BidNft.objects.all().order_by('-id')
        return render(request, self.template_name, {'bids':bids})
    
class EditBids(TemplateView):
    template_name = 'lighthouse/bids/edit.html'
    def get(self, request, id):
        bid = get_object_or_404(BidNft, id=id)
        form = PlaceBidForm(instance=bid)
        return render(request, 'lighthouse/bids/edit.html', {'form': form, 'bid': bid})
    
    def post(self, request, id):
        bid = get_object_or_404(BidNft, id=id)
        form = PlaceBidForm(request.POST or None, instance=bid)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Bid has been updated successfully')
            return redirect('all-bids')
        else:
            messages.error(request, 'Failed to update bid')
            return redirect(request.META.get('HTTP_REFERER'))