# Generated by Django 3.2.8 on 2021-11-01 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipeapp', '0011_recipe_date_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='url',
            field=models.URLField(blank=True),
        ),
    ]
