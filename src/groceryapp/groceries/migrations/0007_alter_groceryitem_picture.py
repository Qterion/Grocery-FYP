# Generated by Django 4.0.7 on 2023-04-26 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groceries', '0006_alter_groceryitem_retailer_alter_groceryitem_similar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groceryitem',
            name='picture',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
