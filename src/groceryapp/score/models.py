from django.db import models
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
from django.db.models import Avg
from django.db.models.signals import post_save
from django.utils import timezone
User=settings.AUTH_USER_MODEL # modded auth user


class ScoreChoice(models.IntegerChoices):
    __empty__="Give Score"
    One=1
    Two=2
    Three=3
    Four=4
    Five=5


class ScoreQuerySet(models.QuerySet):
   
    
    def groceries(self):
        grocery=apps.get_model('groceries',"GroceryItem")
        grocery_content=ContentType.objects.get_for_model(grocery)
        return self.filter(active=True, content_type=grocery_content)

    def as_dict_object(self, object_ids=[]):
        score_qs=self.filter(object_id__in=object_ids)
        return {f"{x.object_id}":x.value for x in score_qs} 
    
    def average(self):
        return self.get_queryset().average()
    
    def get_queryset(self):
        return ScoreQuerySet(self.model, using=self._db)
    
class ScoreManager(models.Manager):
    def get_queryset(self):
        return ScoreQuerySet(self.model, using=self._db)

    def groceries(self):
        return self.get_queryset().groceries()
    def average(self):
        return self.aggregate(average=Avg('value'))['average']
    

class Score(models.Model):
    object_id=models.PositiveBigIntegerField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
    content_obj=GenericForeignKey("content_type","object_id")
    value=models.IntegerField(null=True,blank=True,choices=ScoreChoice.choices)
    active=models.BooleanField(default=True)
    timestamp_active_upt=models.DateTimeField(auto_now_add=False,auto_now=False,null=True,blank=True)
    timestamp=models.DateTimeField(auto_now_add=True)

    objects=ScoreManager()

    class Meta:
        ordering=["-timestamp"]

def score_pst_save(sender,instance,created,*args,**kwargs):
    if created:
        _id=instance.id
        if instance.active:
            score_query=Score.objects.filter(
                user=instance.user,
                content_type=instance.content_type,
                object_id=instance.object_id,
                
                ).exclude(id=_id, active=True)
            if score_query.exists():
                score_query=score_query.exclude(timestamp_active_upt__isnull=False)
                score_query.update(active=False, timestamp_active_upt=timezone.now())
    

post_save.connect(score_pst_save,sender=Score)