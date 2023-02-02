from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.db import transaction
from accounts.models import User

# Create your views here.

class RegisterView(TemplateView):
    template_name = 'auth/register.html'
    def get(self, request):
        return render(request, self.template_name)
    
    @transaction.atomic
    def post(self, request):
        first_name = request.POST['first_name']
        last_name =request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        
        if first_name and last_name and username and email and password and password1:
            if not User.objects.filter(username=username).exists():
                if not User.objects.filter(email=email).exists():
                    if not len(password) < 6:
                        if password == password1:
                            user = User.objects.create(first_name=first_name, last_name=last_name, username=username, email=email, password=password, get_user_p=password1)
                            user.username = username.replace(" ", "")
                            user.set_password(password)
                            user.is_active = False
                            user.save()
                            messages.success(request, 'Account Created successfully')
                            return redirect('home')
                        else:
                            messages.error(request, 'Password does not match')
                            return redirect(request.META.get('HTTP_REFERER'))
                    else:
                        messages.error(request, 'Password cannot be less than 6 characters')
                        return redirect(request.META.get('HTTP_REFERER'))
                else:
                    messages.error(request, 'Email already exists')
                    return redirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, 'Username taken, try another one')
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'All fields must be filled')
            return redirect(request.META.get('HTTP_REFERER'))
    
    

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
                            return redirect('home')
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