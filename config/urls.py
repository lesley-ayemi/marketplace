"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from users.views import *
from accounts.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Page Routes
    path('', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='pages/about.html'), name='about-us'),
    path('faq/', TemplateView.as_view(template_name='pages/faq.html'), name='faq'),
    path('terms-and-condition/', TemplateView.as_view(template_name='pages/about.html'), name='terms-and-condition'),
    path('privacy-policy/', TemplateView.as_view(template_name='pages/privacy-policy.html'), name='privacy-policy'),
    path('contact-us/', TemplateView.as_view(template_name='pages/contact-us.html'), name='contact-us'),
    path('expore/', TemplateView.as_view(template_name='pages/explore.html'), name='explore'),
    path('explore-users/', TemplateView.as_view(template_name='pages/explore-users.html'), name='explore-users'),
    
    
    # Authentication Routes
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    
    
    # Users Routes
    path('users/', include([
        path('', UsersDashboard.as_view(), name='users'),
        path('edit-profile/', EditProfile.as_view(), name='edit-profile'),
        path('update-profile/', UpdateDetails.as_view(), name='update-profile'),
        path('change-password/', ChangePassword.as_view(), name='change-password'),
        
        #NFT routes
        path('create-nft/', UploadNft.as_view(), name='create-nft'),
        path('edit-nft/<slug:slug>/', EditNft.as_view(), name='edit-nft'),
        path('delete-nft/<slug:slug>/', DeleteNft.as_view(), name='delete-nft'),
        path('myarts/<slug:slug>/', UploadNftDetail.as_view(), name='nft_details'),
        
        path('create-collection/', CreateCollection.as_view(), name='create-collection'),
        path('edit-collection/<slug:slug>/', EditCollection.as_view(), name='edit-collection'),
        path('delete-collection/<slug:slug>/', DeleteCollection.as_view(), name='delete-collection'),
        path ('mycollection/<slug:slug>/', ViewCollection.as_view(), name='collections'),
        
        #Wallet
        path('add-wallet/', AddWallet.as_view(), name='add-wallet'),
        path('delete-wallet/<int:id>/', DeleteWallet.as_view(), name='delete-wallet'),
        
        #Deposit
        path('deposit-funds/', FundAccount.as_view(), name='fund-account'),
        path('deposit-funds/<str:name>/', FundAccountDetail.as_view(), name='fund-account-details'),
        
        #Withdraw
        path('withdraw-funds/', WithdrawAccount.as_view(), name='withdraw-funds'),
    ]))
    
    # Lighthouse Admin Routes
    
    
]
if settings.DEBUG:
        urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)