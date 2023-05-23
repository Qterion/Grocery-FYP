from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import os
from django.contrib.contenttypes.fields import GenericRelation
from score.models import Score
import datetime
from django.db.models import Q
SCORE_TIMER_DAYS=3

class GroceryQuerySet(models.QuerySet):
    def require_update(self):
        current_time=timezone.now()
        days_passed=current_time-datetime.timedelta(days=SCORE_TIMER_DAYS)
        return self.filter(
            Q(score_last_update__gte=days_passed)|
            Q(score_last_update__isnull=True)
        )

class GroceryItemManager(models.Manager):
    def get_queryset(self,*args,**kwargs):

        return GroceryQuerySet(self.model,using=self._db)

    def require_update(self):
        return self.get_queryset().require_update()


class GroceryItem(models.Model):
    title=models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    ingredients = models.CharField(max_length=2000, null=True, blank=True)
    price=models.FloatField(blank=True, null=True)
    category=models.CharField(max_length=200,null=True,blank=True)
    link=models.URLField(max_length=200,blank=True,null=True)
    status=models.CharField(max_length=20, null=True, blank=True, default="active")
    picture_filename = models.CharField(max_length=255, null=True, blank=True)
    last_update=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    retailer=models.CharField(max_length=100, null=True)
    gluten_free=models.BooleanField(blank=True,null=True)
    lactose_free=models.BooleanField(blank=True,null=True)
    nut_free=models.BooleanField(blank=True,null=True)
    similar=models.URLField(max_length=200,blank=True, null=True)
    score=GenericRelation(Score)
    score_last_update=models.DateTimeField(auto_now=False,auto_now_add=False,blank=True,null=True)
    score_count=models.IntegerField(blank=True,null=True)
    average_score=models.DecimalField(decimal_places=2,max_digits=5,blank=True,null=True)
    objects=GroceryItemManager()


   

    def to_dict(self):
        return{

            'title':self.title,
            'description':self.description,
            'last_update':self.last_update,
            'price':self.price,
            'picture': self.picture,
            'retailer':self.retailer,
            'id':self.id

        }
    def __str__(self):
        return f"{self.title} ({self.retailer})"
    def display_average_score(self):
        now=timezone.now()
        if not self.score_last_update:
            return self.compute_score()
        if self.score_last_update>now-datetime.timedelta(days=SCORE_TIMER_DAYS):
            return self.average_score
        return self.compute_score()

    def compute_score_average(self):
        return self.score.average()

    def compute_score_count(self):
        return self.score.all().count()

    def compute_score(self, save=True):
        self.average_score=self.compute_score_average()
        self.score_count=self.compute_score_count()
        self.score_last_update=timezone.now()
        if save:
            self.save()
        return self.average_score

    def get_absolute_url(self):
        return f"/groceries/{self.id}/"
    

    @staticmethod
    def get_all_items():
        return GroceryItem.objects.all()

    
    @staticmethod
    def get_items_by_id(id):
        return GroceryItem.objects.filter(id__in=id)

    @staticmethod
    def get_items_by_category(cat):
        if cat:
            return GroceryItem.objects.filter(category=cat)
        else:
            return GroceryItem.get_all_items()

# class Basket(models.Model):
#     product = models.ForeignKey(GroceryItem,
#                                 on_delete=models.CASCADE)
#     customer = models.ForeignKey(CustomUser,
#                                  on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)
#     price = models.IntegerField()
#     status = models.BooleanField(default=False)
  
#     def placeOrder(self):
#         self.save()
  
#     @staticmethod
#     def get_orders_by_customer(customer_id):
#         return Basket.objects.filter(customer=customer_id).order_by('price')
