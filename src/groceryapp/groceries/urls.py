from django.contrib import admin  
from django.urls import path  
from django.urls.conf import include  
from django.conf import settings  
from django.conf.urls.static import static

from . import views
urlpatterns = [
    path("", views.view_grocery_list),
    path("<int:pk>/", views.view_grocery_detail),
    
]   

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)