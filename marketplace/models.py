from django.db import models
from mutual.models import TimeStampedModel
from accounts.models import User
from django.urls import reverse
from autoslug import AutoSlugField
from autoslug.settings import slugify as default_slugify
from cloudinary.models import CloudinaryField
from .utils import unique_order_id_generator
from django.db.models.signals import pre_save

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
    order_id = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator_nft', blank=True, null=True)
    # autoslugify value using custom `slugify` function
    def custom_slugify(value):
        return default_slugify(value).replace('-', '_')
    
    slug = AutoSlugField(populate_from='name',
                         unique_with=['created__month'],
                         slugify=custom_slugify)
    description = models.TextField()
    item_price = models.FloatField()
    size = models.CharField(blank=True, max_length=100)
    upload_nft = models.FileField(blank=True, null=True, default='https://res.cloudinary.com/dbbfeegje/image/upload/v1674443265/coll-item-2_vqfk6q.jpg')
    # upload_nft = CloudinaryField(resource_type='raw', folder = "/nft-items/", blank=True, default='https://res.cloudinary.com/dbbfeegje/image/upload/v1674443265/coll-item-2_vqfk6q.jpg')
    properties = models.CharField(max_length=255, blank=True)
    royalties = models.CharField(max_length=100, blank=True)
    collection = models.ForeignKey('NftCollection', on_delete=models.SET_NULL, blank=True, null=True, related_name='nft_collections')
    nft_type = models.CharField(max_length=100, choices=NFT_TYPE.choices, default='art')
    bid = models.CharField(max_length=5, choices=ALLOW_BID, default='NO')
    purchased_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='purchased_by_user')
    status = models.CharField(max_length=10, choices=ITEM_STATUS, default='BUY')
    list_for_sale = models.BooleanField(default=True)
    minted = models.BooleanField(default=False)
    gas_fee = models.FloatField(default=0.18)
    mint_proof = models.FileField(null=True, blank=True)
    
    def __str__(self):
        return self.name + '- NFT'
    
    def get_absolute_url(self):
        return reverse("nft_details", kwargs={"slug": self.slug})
    
def pre_save_create_order_id(sender, instance, *args, **kwargs):
        if not instance.order_id:
            instance.order_id= unique_order_id_generator(instance)


pre_save.connect(pre_save_create_order_id, sender=CreateNftModel)
    # slug = AutoSlugField()

    
    
class BidNft(models.Model):
    bid_item = models.OneToOneField(CreateNftModel, on_delete=models.DO_NOTHING)
    bid_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    bid_amount = models.FloatField()
    end_bid = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.bid_item)
    
    # def save(self, *args, **kwargs):
    #     try:
    #         bid_item = CreateNftModel.objects.filter(bid='YES').get()
            
    #         # if self.id is None:
    #     except Exception as e:
    #         print (e)
    #         super(BidNft, self).save(*args, **kwargs)
                
    

class NftCollection(TimeStampedModel):
    class BlockChainType(models.TextChoices):
        Ethereum = 'ethereum'
        Polygon = 'polygon'
        Solana = 'solana'
    logo_image = models.ImageField(blank=True, null=True, default='')
    banner_image = models.ImageField(blank=True, null=True, default='')
    featured_image = models.ImageField(blank=True, null=True, default='')
    name = models.CharField(max_length=100)
    custom_url = models.URLField(blank=True, null=True)
    # autoslugify value using custom `slugify` function
    def custom_slugify(value):
        return default_slugify(value).replace('-', '_')
    slug = AutoSlugField(populate_from='name',
                         slugify=custom_slugify)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.DO_NOTHING, related_name='user_category')
    creator_earning = models.CharField(blank=True, null=True, max_length=20)
    payout_address = models.CharField(max_length=100, blank=True, null=True)
    blockchain = models.CharField(max_length=40, choices=BlockChainType.choices, default='ethereum')
    sensitive_content = models.BooleanField(default=False)
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