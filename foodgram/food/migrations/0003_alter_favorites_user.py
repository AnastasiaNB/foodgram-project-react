# Generated by Django 4.1.4 on 2022-12-25 19:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0002_alter_amount_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorites',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.user'),
        ),
    ]