# Generated by Django 4.1.4 on 2023-01-02 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0002_alter_favorites_user_alter_recipe_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(upload_to='food/images', verbose_name='Фото блюда'),
        ),
    ]
