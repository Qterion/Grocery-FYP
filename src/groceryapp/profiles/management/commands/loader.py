from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from groceryapp import utils as grocery_utils
from groceries.models import GroceryItem
User=get_user_model()
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("count", nargs='?',default=5000, type=int)
        parser.add_argument("--groceries", action='store_true',default=False)
        parser.add_argument("--users", action='store_true',default=False)
        parser.add_argument("--show-total", action='store_true',default=False)
    def handle(self,*args,**options):
        print(f"Hello there are {User.objects.count()} users")
        count=options.get('count')
        show_total=options.get('show_total')
        load_groceries=options.get('groceries')
        create_users=options.get('users')
        if load_groceries:
            groceries_dataset=grocery_utils.load_grocery_data(limit=count)
            
            counter=0
            
            for grocery in groceries_dataset:
                # new_users.append(User(**user))
                
                try:
                    new_grocery=GroceryItem.objects.create(**grocery)
                    print(new_grocery)
                    counter+=1
                except:
                    continue                    
            print(f"{counter} groceries added")
        if create_users:
            users=grocery_utils.get_fake_users(count)
            counter=0
            for user in users:
                # new_users.append(User(**user))
                try:
                    User.objects.create(**user)
                    counter+=1
                except:
                    continue
            print(str(counter)+" users created")
        # bulk_of_users=User.objects.bulk_create(users, ignore_conflicts=True)
        # print(f"New users created {len(bulk_of_users)}")
        