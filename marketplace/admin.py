from django.contrib import admin
from .models import CreateNftModel, NftCollection, Category, BidNft

# Register your models here.
admin.site.register(CreateNftModel)
admin.site.register(NftCollection)
admin.site.register(Category)
admin.site.register(BidNft)