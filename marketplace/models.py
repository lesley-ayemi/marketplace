from django.db import models
from mutual.models import TimeStampedModel
from accounts.models import User
from django.urls import reverse
from autoslug import AutoSlugField


class CreateNftModel(TimeStampedModel):
    ALLOW_BID = (
        ('YES', 'YES'),
        ('NO', 'NO'),
    )
    ITEM_STATUS = (
        ('BUY', 'BUY'),
        ('SOLD', 'SOLD'),
    )
    name = models.CharField(max_length=100)
    creator = models.ForeignKey('User', on_delete=models.DO_NOTHING, related_name='creator_nft', blank=True, null=True)
    slug = AutoSlugField(populate_from=lambda instance: instance.name,
                         unique_with=['created__month'],
                         slugify=lambda value: value.replace(' ','-'))
    description = models.TextField()
    item_price = models.FloatField()
    size = models.CharField(blank=True)
    properties = models.CharField(max_length=255, blank=True)
    royalties = models.CharField(max_length=100, blank=True)
    collection = models.ForeignKey('NftCollection', on_delete=models.DO_NOTHING, blank=True, related_name='nft_collections')
    bid = models.CharField(max_length=5, choices=ALLOW_BID, default='')
    status = models.CharField(max_length=10, choices=ITEM_STATUS, default='BUY')
    minted = models.BooleanField(default=False)
    gas_fee = models.FloatField(default=0.018)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("nft_details", kwargs={"slug": self.slug})
    

class NftCollection(TimeStampedModel):
    logo_image = models.ImageField()
    banner_image = models.ImageField()
    featured_image = models.ImageField()
    name = models.CharField(max_length=100)
    slug = models.AutoSlugField(populate_from=lambda instance: instance.name,
                         slugify=lambda value: value.replace(' ','-'))
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
    slug = models.AutoSlugField(populate_from=lambda instance: instance.name,
                         slugify=lambda value: value.replace(' ','-'))
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("categories", kwargs={"slug": self.slug})