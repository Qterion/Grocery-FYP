# Generated by Django 4.0.7 on 2023-04-26 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groceries', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='groceryitem',
            name='similar',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
