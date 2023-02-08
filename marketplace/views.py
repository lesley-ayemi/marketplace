from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect
from .models import *
from accounts.models import User

# Create your views here.

"""Explore NFTs"""
class ExploreNft(TemplateView):
    template_name = 'pages/explore.html'
    def get(self, request):
        all_nfts = CreateNftModel.objects.filter(Q(list_for_sale=True) and Q(minted=True)).order_by('created').values('name', 'creator', 'item_price', 'upload_nft', 'status', 'nft_type', 'slug').distinct()
        context = {
            'all_nfts':all_nfts,
        }
        return render(request, self.template_name, context)
    
    
"""Product Details"""
class ExploreNftPageDetail(TemplateView):
    template_name = 'pages/explore-detail.html'
    def get(self, request, slug):
        nft = get_object_or_404(CreateNftModel, slug=slug)
        bids = BidNft.objects.filter(bid_item_id=nft.id)
        context = {
            'nft':nft,
            'bids':bids,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, slug):
        nft = get_object_or_404(CreateNftModel, slug=slug)
        user = get_object_or_404(User, uuid=self.request.user.uuid)
        seller = get_object_or_404(User, uuid=nft.creator.uuid)

        if user:
            if user.balance >= nft.item_price:
                user.balance -= nft.item_price
                user.save()
                nft.status = 'SOLD'
                nft.purchased_by = user
                nft.save()
                seller.balance += nft.item_price
                seller.save()
                messages.success(request, 'NFT purchased successfully')
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, 'Fund account, balance is too low to purchase NFT')
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'Error, try logging in again')
            return redirect('login')
        
                
"""Place Bid"""
class PlaceBid(TemplateView):
    def post(self, request, id):
        nft = get_object_or_404(CreateNftModel, id=id)
        # get_bid = get_object_or_404(BidNft, bid_item=nft)
        get_bid = BidNft.objects.filter(bid_item=nft)
        amount = request.POST['bid_amount']
        
        if amount:
            if amount != 0:
                if nft:
                    if get_bid:
                        bid_nft = BidNft.objects.get(bid_item=nft)
                        bid_nft.bid_user = self.request.user
                        bid_nft.bid_amount += float(amount)
                        bid_nft.save()
                        messages.success(request, 'Bid placed successfully')
                        return redirect(request.META.get('HTTP_REFERER'))
                    else:
                        BidNft.objects.create(bid_item=nft, 
                                              bid_user=request.user, 
                                              bid_amount=float(amount)).save()
                        messages.success(request, 'Bid Created successfully')
                        return redirect(request.META.get('HTTP_REFERER'))
                else:
                    messages.error(request, 'Failed to fetch NFT')
                    return redirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, '0 cannot be placed as a bid')
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'Amount cannot be left blank')
            return redirect(request.META.get('HTTP_REFERER'))
        
        
"""Search NFT"""
class SearchNft(ListView):
    # template_name = 'pages/search.html'
    # def get(self, request):
    #     all_nfts = CreateNftModel.objects.filter(Q(list_for_sale=True) and Q(minted=True)).order_by('created').values('name', 'creator', 'item_price', 'upload_nft','status', 'nft_type','slug').distinct()
    #     context = {
    #         'all_nfts':all_nfts,
    #     }
    #     return render(request, self.template_name, context)
    
    # def post(self, request):
    #     search_term = request.POST['search_term']
    model = CreateNftModel
    template_name = 'pages/search-nft.html'
    
    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = CreateNftModel.objects.filter(
            Q(name__icontains=query) | 
            Q(creator__username__icontains=query) | 
            Q(purchased_by__username__icontains=query), 
            minted=True)
        return object_list
    
    
class ExploreUsers(TemplateView):
    template_name = 'pages/explore-users.html'
    def get(self, request):
        all_users = User.objects.filter(is_user=True)
        # get_total = CreateNftModel.objects.filter(user=all_users)
        context = {
            'all_users':all_users,
        }
        return render(request, self.template_name, context)
    
    
class ExploreUsersDetailView(TemplateView):
    template_name = 'pages/explore-users-detail.html'
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        all_nfts = CreateNftModel.objects.filter(creator=user)
        context = {
            'user':user,
            'all_nfts':all_nfts,
        }
        return render(request, self.template_name, context)