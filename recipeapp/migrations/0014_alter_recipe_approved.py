# Generated by Django 3.2.8 on 2021-11-09 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipeapp', '0013_alter_recipe_about'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='approved',
            field=models.BooleanField(default=True),
        ),
    ]
