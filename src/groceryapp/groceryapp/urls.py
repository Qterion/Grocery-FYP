from django.contrib import admin  
from django.urls import path  
from django.urls.conf import include  
from django.conf import settings  
from django.conf.urls.static import static
from profiles import views
from groceries import views as grocery_view
from score import views as score_view
urlpatterns = [
    path("", views.mainpage, name="mainpage"),
    path("groceries/",include("groceries.urls")),
    path('admin/', admin.site.urls),
    path("signup/",views.signup_request,name="signup"),
    path("signin/", views.signin_request, name="signin"),
    path('signout/',views.signout_user,name='signout'),
    path('score/grocery/',score_view.view_grocery_score, name="vgrc_score"),
    path("search/", grocery_view.search_items, name="search"),
]   

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)