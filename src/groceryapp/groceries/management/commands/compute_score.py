from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from groceryapp import utils as grocery_utils
from score.tasks import grocery_score_change_task
from groceries.models import GroceryItem
User=get_user_model()
class Command(BaseCommand):
    def handle(self,*args,**options):
        grocery_score_change_task()
        