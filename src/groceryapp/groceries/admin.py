from django.contrib import admin
from .models import GroceryItem

class GroceryAdmin(admin.ModelAdmin):
    list_display=["__str__","average_score","score_last_update"]
    readonly_fields=['average_score',"score_count","display_average_score"]


admin.site.register(GroceryItem, GroceryAdmin)