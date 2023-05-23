from django.contrib import admin

from .models import Score

class ScoreAdmin(admin.ModelAdmin):
    list_display=['content_obj','user','value','active']
    raw_id_fields=['user']
    readonly_fields=['content_obj']
    search_fields=['user__username']

admin.site.register(Score,ScoreAdmin)