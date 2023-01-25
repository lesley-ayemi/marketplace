from django.db import models
from mutual.models import TimeStampedModel
from accounts.models import User
from django.urls import reverse
from autoslug import AutoSlugField
from autoslug.settings import slugify as default_slugify
from cloudinary.models import CloudinaryField

class CreateNftModel(TimeStampedModel):
    ALLOW_BID = (
        ('YES', 'YES'),
        ('NO', 'NO'),
    )
    ITEM_STATUS = (
        ('BUY', 'BUY'),
        ('SOLD', 'SOLD'),
    )
    class NFT_TYPE(models.TextChoices):
        Art = 'art'
        Video = 'video'
        Music = 'music'
        Trading_card_or_collectible = 'trading-cards/collectible'
        Text = 'text'
        Memes = 'memes'
        Domain_name = 'domain-name'
        Virtual_style = 'virtual-style'
        Pdf = 'pdf'
    # NFT_TYPE = (
    #     ('art', 'art'),
    #     ('video', 'video'),
    #     ('music', 'music'),
    #     ('trading-cards/collectible', 'trading-cards/collectible'),
    #     ('text', 'text'),
    #     ('memes', 'memes'),
    #     ('domain-names', 'domain-names'),
    #     ('virtual-style', 'virtual-style'),
    #     ('incidental-internet-based-things', 'incidental-internet-based-things'),
    #     ('pdf', 'pdf'),
    # )
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='creator_nft', blank=True, null=True)
    # autoslugify value using custom `slugify` function
    def custom_slugify(value):
        return default_slugify(value).replace('-', '_')
    
    slug = AutoSlugField(populate_from='name',
                         unique_with=['created__month'],
                         slugify=custom_slugify)
    description = models.TextField()
    item_price = models.FloatField()
    size = models.CharField(blank=True, max_length=100)
    upload_nft = CloudinaryField('raw', folder = "/nft-items/", blank=True, default='https://res.cloudinary.com/dbbfeegje/image/upload/v1674443265/coll-item-2_vqfk6q.jpg')
    properties = models.CharField(max_length=255, blank=True)
    royalties = models.CharField(max_length=100, blank=True)
    collection = models.ForeignKey('NftCollection', on_delete=models.SET_NULL, blank=True, null=True, related_name='nft_collections')
    nft_type = models.CharField(max_length=100, choices=NFT_TYPE.choices, default='art')
    bid = models.CharField(max_length=5, choices=ALLOW_BID, default='NO')
    purchased_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='purchased_by_user')
    status = models.CharField(max_length=10, choices=ITEM_STATUS, default='BUY')
    list_for_sale = models.BooleanField(default=True)
    minted = models.BooleanField(default=False)
    gas_fee = models.FloatField(default=0.018)
    
    def __str__(self):
        return self.name + '- NFT'
    
    def get_absolute_url(self):
        return reverse("nft_details", kwargs={"slug": self.slug})
    
    
    # slug = AutoSlugField()

    
    
class BidNft(models.Model):
    bid_item = models.OneToOneField(CreateNftModel, on_delete=models.DO_NOTHING)
    bid_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    bid_amount = models.FloatField()
    end_bid = models.BooleanField(default=False)
    
    def __str__(self):
        return self.bid_item
    

class NftCollection(TimeStampedModel):
    logo_image = CloudinaryField('image', folder = "/collection-images/logo/")
    banner_image = CloudinaryField('raw', folder = "/collection-images/bannger/")
    featured_image = CloudinaryField('image')
    name = models.CharField(max_length=100)
    # autoslugify value using custom `slugify` function
    def custom_slugify(value):
        return default_slugify(value).replace('-', '_')
    slug = AutoSlugField(populate_from='name',
                         slugify=custom_slugify)
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.DO_NOTHING, related_name='user_category')
    user_collection = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user_collections')
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("collections", kwargs={"slug": self.slug})
    
    
class Category(models.Model):
    # class CategoryOptions(models.TextChoices):
        
    # CATEGORY_OPTIONS = (
    #     ('art', 'art'),
    #     ('domain names', 'domain names'),
    #     ('gaming', 'gaming'),
    #     ('membership'),
    #     ('music'),
    #     ('PFPs'),
    #     ('photography'),
    #     ('sport collectables'),
    #     ('virtual worlds', ''),
    # )
    name = models.CharField(max_length=100)
    # category_type = models.TextChoices('ART', 'DOMAIN NAME', 'GAMING', 'MEMBERSHIP', 'MUSIC', 'PFPs', 'PHOTOGRAPHY', 'SPORT COLLECTABLES', 'VIRTUAL WORLDS')
    # autoslugify value using custom `slugify` function
    def custom_slugify(value):
        return default_slugify(value).replace('-', '_')
    slug = AutoSlugField(populate_from='name',
                         slugify=custom_slugify)
    
    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
        return reverse("categories", kwargs={"slug": self.slug})