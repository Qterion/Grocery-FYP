from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.db.models import Q
from django.views import generic

from .models import GroceryItem

SORT_PARAMS={
    "rand recommendations":'?',
    "Descending reccomendations":'-average_score',
    "Ascending reccomendations":'average_score',
    "latest uploaded items":'-last_update',
    
}

class ViewGroceriesList(generic.ListView):
    paginate_by=90
    queryset=GroceryItem.objects.all().order_by('-average_score')

    def get_queryset(self):
        request=self.request
        default_srt=request.session.get('grc_sort_order') or '-average_score'
        
        
        if default_srt!="-last_update":
            query_set=GroceryItem.objects.all().order_by(default_srt)
            query_set=self.recommendations_sort(query_set=query_set,request=request)
        else:
            query_set=GroceryItem.objects.all().order_by(default_srt)
        sort=request.GET.get('sort')
        if sort is not None:
            if sort!="-last_update":
                query_set=self.recommendations_sort(query_set=query_set,request=request)
                request.session['grc_sort_order']="?"
            else:    
                request.session['grc_sort_order']=sort
            query_set=query_set.order_by(sort)
        return query_set
    
    def recommendations_sort(self,query_set):
        if self.request.user.gluten_trigger:
            query_set=query_set.filter(gluten_free=True)
        if self.request.user.lactose_trigger:
            query_set=query_set.filter(lactose_free=True)
        if self.request.user.nut_trigger:
            query_set=query_set.filter(nut_free=True)

        return query_set

    def get_template_names(self):
        request=self.request
        if request.htmx:
            return['groceries/snippets/list.html']
        return ['groceries/view_list.html']

    def get_context_data(self,*args ,**kwargs) -> Dict[str, Any]:
        context=super().get_context_data(*args,**kwargs)
        request=self.request
        user=request.user
        context["sort_params"]=SORT_PARAMS
        if user.is_authenticated:
            object_list=context["object_list"]
            object_id_list=[x.id for x in object_list]
            
            context['my_scores']=user.score_set.groceries().as_dict_object(object_ids=object_id_list)
        return context
    
                
view_grocery_list=ViewGroceriesList.as_view()

def search_items(request):
    q=request.GET['q']
    data=GroceryItem.objects.filter(title__icontains=q,).order_by("-average_score")
    return render(request,'groceries/search.html',{'object_list':data})
                

class ViewGroceryDetail(generic.DetailView):
    template_name="groceries/detail.html"
    queryset=GroceryItem.objects.all()

    def get_context_data(self,*args ,**kwargs) -> Dict[str, Any]:
        context=super().get_context_data(*args,**kwargs)
        request=self.request
        user=request.user
        
        if user.is_authenticated:
            object=context["object"]
            object_id_list=[object.id]
            similar=object.similar
            
            if len(similar)>3:
                sim_obj=GroceryItem.objects.get(link=similar)
                
                context["similar_object"]=sim_obj
            else:
                context["similar_object"]=None
            
            context['my_scores']=user.score_set.groceries().as_dict_object(object_ids=object_id_list)
        return context
view_grocery_detail=ViewGroceryDetail.as_view()