from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from groceries.models import GroceryItem
from .models import Score
# Create your views here.
def view_grocery_score(request):
    if not request.htmx:
        return HttpResponse("HTMX request reuqired", status=400)
    obj_id=request.POST.get('object_id')
    score_val=request.POST.get('score_value')
    user=request.user
    msg="Not authenticated"
    if request.user.is_authenticated:
        msg="<span class='bg-danger text-light py-1 px-3'>Error</span>"
        ctype=ContentType.objects.get_for_model(GroceryItem)
        score_object=Score.objects.create(content_type=ctype,object_id=obj_id, value=score_val,user=user)
        if score_object.content_obj is not None:
            msg="<span class='bg-success text-light py-1 px-3'>Updated!</span>"
    return HttpResponse(msg,status=200)