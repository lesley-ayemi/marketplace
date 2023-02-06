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
from django.urls import path, include, re_path as url
from django.conf import settings
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from lighthouse.views import *
from django.views.static import serve

from users.views import *
from accounts.views import *
from marketplace.views import *
urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path('admin/', admin.site.urls),
    
    # Page Routes
    path('', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='pages/about.html'), name='about-us'),
    path('faq/', TemplateView.as_view(template_name='pages/faq.html'), name='faq'),
    path('terms-and-condition/', TemplateView.as_view(template_name='pages/terms-and-condition.html'), name='terms-and-condition'),
    path('privacy-policy/', TemplateView.as_view(template_name='pages/privacy-policy.html'), name='privacy-policy'),
    path('contact-us/', TemplateView.as_view(template_name='pages/contact-us.html'), name='contact-us'),
    path('explore/', ExploreNft.as_view(), name='explore'),
    path('explore/<slug:slug>/', ExploreNftPageDetail.as_view(), name='explore-detail'),
    path('explore/bid/<int:id>/', PlaceBid.as_view(), name='place-bid'),
    path('explore-users/', ExploreUsers.as_view(), name='explore-users'),
    
    #Search Routes
    path('search/', SearchNft.as_view(), name='search-nft'),
    
    
    # Authentication Routes
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    
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
    ])),
    
    # Lighthouse Admin Routes
    path('lighthouse/', include([
        path('', LighthouseDashboard.as_view(), name='lighthouse'),
        
        path('categories/', Categories.as_view(), name='categories'),
        path('edit-category/<str:slug>/', EditCategory.as_view(), name='edit-category'),
        
        path('all-users/', AllUsers.as_view(), name='all-users'),
        path('edit-user/<str:username>/', EditUser.as_view(), name='edit-user'),
        path('delete-user/<str:username>/', DeleteUser.as_view(), name='delete-user'),
        path('all-wallets/', AllWalletUsers.as_view(), name='all-wallets'),
        path('create-user/', CreateUser.as_view(), name='create-user'),
        
        #NFTS
        path('all-nfts/', AllNft.as_view(), name='all-nfts'),
        path('create-nfts/', CreateNft.as_view(), name='create-nfts'),
        path('unminted-nfts/', UnmintedNft.as_view(), name='unminted-nfts'),
        path('edit-unminted-nft/<str:slug>/', EditUnmintedNft.as_view(), name='edit-unminted-nft'),
        path('admin-edit-nft/<str:slug>/', AdminEditNft.as_view(), name='admin-edit-nft'),
        path('admin-delete-nft/<str:slug>/', AdminDeleteNft.as_view(), name='admin-delete-nft'),
        
        path('approved-deposits/', ApprovedDeposits.as_view(), name='approved-deposits'),
        path('pending-deposits/', PendingDeposits.as_view(), name='pending-deposits'),
        path('declined-deposits/', DeclinedDeposits.as_view(), name='declined-deposits'),
        
        path('approved-withdrawals/',ApprovedWithdrawals.as_view(), name='approved-withdrawals'),
        path('pending-withdrawals/',PendingWithdrawals.as_view(), name='pending-withdrawals'),
        path('declined-withdrawals/',DeclinedWithdrawals.as_view(), name='declined-withdrawals'),
        
        path('add-payment-method/', AddPaymentMethod.as_view(), name='add-payment-method'),
        # path('edit-profile/', EditProfile.as_view(), name='edit-profile'),
        # path('update-profile/', UpdateDetails.as_view(), name='update-profile'),
        # path('change-password/', ChangePassword.as_view(), name='change-password'),
        
        # #NFT routes
        # path('create-nft/', UploadNft.as_view(), name='create-nft'),
        # path('edit-nft/<slug:slug>/', EditNft.as_view(), name='edit-nft'),
        # path('delete-nft/<slug:slug>/', DeleteNft.as_view(), name='delete-nft'),
        # path('myarts/<slug:slug>/', UploadNftDetail.as_view(), name='nft_details'),
    ])),
    
    
]
if settings.DEBUG:
        urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
        urlpatterns += static(settings.MEDIA_URL,
                        document_root=settings.MEDIA_ROOT)