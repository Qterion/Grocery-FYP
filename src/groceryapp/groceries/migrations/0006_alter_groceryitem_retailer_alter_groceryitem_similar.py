# Generated by Django 4.0.7 on 2023-04-26 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groceries', '0005_alter_groceryitem_retailer_alter_groceryitem_similar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groceryitem',
            name='retailer',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='groceryitem',
            name='similar',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
