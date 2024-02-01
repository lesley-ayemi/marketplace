from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.db import transaction
from accounts.forms import SignUpForm
from accounts.models import User


from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from config import settings
# Create your views here.

# class RegisterView(TemplateView):
#     template_name = 'auth/register.html'
#     def get(self, request):
#         return render(request, self.template_name)
    
#     @transaction.atomic
#     def post(self, request):
#         first_name = request.POST['first_name']
#         last_name =request.POST['last_name']
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']
#         password1 = request.POST['password1']
        
#         if first_name and last_name and username and email and password and password1:
#             if not User.objects.filter(username=username).exists():
#                 if not User.objects.filter(email=email).exists():
#                     if not len(password) < 6:
#                         if password == password1:
#                             user = User.objects.create(first_name=first_name, last_name=last_name, username=username, email=email, password=password, get_user_p=password1)
#                             user.username = username.replace(" ", "")
#                             user.set_password(password)
#                             user.is_active = False
#                             user.save()
#                             messages.success(request, 'Account Created successfully')
#                             return redirect('home')
#                         else:
#                             messages.error(request, 'Password does not match')
#                             return redirect(request.META.get('HTTP_REFERER'))
#                     else:
#                         messages.error(request, 'Password cannot be less than 6 characters')
#                         return redirect(request.META.get('HTTP_REFERER'))
#                 else:
#                     messages.error(request, 'Email already exists')
#                     return redirect(request.META.get('HTTP_REFERER'))
#             else:
#                 messages.error(request, 'Username taken, try another one')
#                 return redirect(request.META.get('HTTP_REFERER'))
#         else:
#             messages.error(request, 'All fields must be filled')
#             return redirect(request.META.get('HTTP_REFERER'))

# Sign Up View
domain_name = settings.DOMAIN_NAME
class RegisterView(View):
    form_class = SignUpForm
    template_name = 'auth/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data['password1']
            user = form.save(commit=False)
            user.get_user_p = password1
            user.set_password(password1)
            user.is_active = True # Deactivate account till it is confirmed
            user.save()

            # current_site = get_current_site(request)
            # subject = f'Activate Your {domain_name} Account'
            # message = render_to_string('emails/account_activation_email.html', {
            #     'user': user,
            #     'domain': current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': account_activation_token.make_token(user),
            # })
            # user.email_user(subject, message)

            # messages.success(request, ('Please Confirm your email to complete registration. Note: check spam if mail is not on inbox'))
            messages.success(request, ('Account Created Successfully'))

            return redirect('login')

        return render(request, self.template_name, {'form': form})    
    
    
class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            # user = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('users')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('login')
    

class LoginView(TemplateView):
    template_name = 'auth/login.html'
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        authenticate(request, username=username, password=password)
        
        if username and password:
            user = User.objects.filter(Q(username=username)).order_by('uuid').first()
            if user is not None:
                if user and check_password(password, user.password):
                    if user.is_active == True:
                        if user.is_user:
                            login(request, user)
                            return redirect('users')
                        elif user.is_admin == True:
                            login(request, user)
                            return redirect('lighthouse')
                        else:
                            messages.error(request, 'You have role')
                            return redirect(request.META.get('HTTP_REFERER'))
                    else:
                        messages.error(request, 'Your account is inactive, contact admin')
                        return redirect(request.META.get('HTTP_REFERER'))
                else:
                    messages.error(request, 'Incorrect Username or Password')
                    return redirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, 'Account not found, Register Account')
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'Username and password required')
            return redirect(request.META.get('HTTP_REFERER'))
        
        
class LogoutView(TemplateView):
    def get(self, request):
        logout(request)
        messages.info(request, 'Logged out')
        return redirect('login')