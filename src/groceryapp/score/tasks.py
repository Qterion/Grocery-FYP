import random
from celery import shared_task
from django.contrib.auth import get_user_model
from groceries.models import GroceryItem
from .models import Score, ScoreChoice
from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg, Count
from django.utils import timezone
import time
import datetime
User=get_user_model()

@shared_task(name="create_fake_scores")
def create_fake_scores(count=200 ,users=20,null_average=False):
    user_start=User.objects.first()
    user_end=User.objects.last()
    rand_user_ids=random.sample(range(user_start.id,user_end.id),users)
    users=User.objects.filter(id__in=rand_user_ids)

    groceries=GroceryItem.objects.all().order_by("?")[:count]
    grocery_content_type=ContentType.objects.get_for_model(GroceryItem)
    if null_average:
        groceries=GroceryItem.objects.filter(average_score__isnull=True).order_by("?")[:count]

    
    score_choices=[i for i in ScoreChoice.values if i is not None]
    number_of_scores=groceries.count()
    user_scores=[random.choice(score_choices) for _ in range(0,number_of_scores)]
    new_score=[]
    for grocery in groceries:
        try:
            tmp=user_scores.pop()
            
            score_object=Score.objects.create(
            user=random.choice(users),
            # object_id=grocery.id,
            # content_type=grocery_content_type,
            content_obj=grocery,
            value=tmp,
            
                )
            new_score.append(score_object.id)
            
        except:
            continue
    return new_score

@shared_task(name="grocery_score_change_task")
def grocery_score_change_task(object_id=None):
    start_t=time.time()
    cont_type=ContentType.objects.get_for_model(GroceryItem)
    score_filter=Score.objects.all().filter(content_type=cont_type)
    if object_id!=None:
        score_filter=Score.objects.all().filter(object_id=object_id)
    aggregate_scores=score_filter.values("object_id","content_type").annotate(average=Avg('value'), count=Count('object_id') )      
    for aggregate_score in aggregate_scores:
        score_id=aggregate_score['object_id']
        score_average=aggregate_score['average']
        count_score=aggregate_score['count']
        grocery_qs=GroceryItem.objects.filter(id=score_id)

        grocery_qs.update(
            score_last_update=timezone.now(),
            score_count=count_score,
            average_score=score_average,


        )
    end_t=time.time()-start_t
    delta=datetime.timedelta(seconds=int(end_t))
    print("Time spent on scoring: "+str(delta)+" ("+str(end_t)+"s)")