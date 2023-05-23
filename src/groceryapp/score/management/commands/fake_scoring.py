from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from groceryapp import utils as grocery_utils
from score.tasks import create_fake_scores
from score.models import Score
User=get_user_model()
# python manage.py fake_scoring 4500 --users 120 --show-total
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("count", nargs='?',default=9000, type=int)
        parser.add_argument("--users",default=1000, type=int)
        parser.add_argument("--show-total", action='store_true',default=False)
    def handle(self,*args,**options):
        count=options.get('count')
        show_total=options.get('show_total')
        load_groceries=options.get('groceries')
        users_amount=options.get('users')
        print(count,show_total, users_amount)
        num_scores=create_fake_scores(count=count, users=users_amount)
        print(f"New scores:{len(num_scores)}")
        if show_total:
            all_scores=Score.objects.all()
            print(f"Total scored:{all_scores.count()}")
        
        