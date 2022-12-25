import os
from pathlib import Path
import json
from django.core.management.base import BaseCommand
from food.models import Ingredient, Tag
from foodgram.settings import BASE_DIR

DATA_DIR = os.path.join(BASE_DIR, 'data')

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(os.path.join(DATA_DIR, 'ingredients.json'), encoding='utf-8') as data:
            ingredients = json.loads(data.read())
            for ingredient in ingredients:
                Ingredient.objects.get_or_create(**ingredient)
        with open(os.path.join(DATA_DIR, 'tags.json'), encoding='utf-8') as data:
            tags = json.loads(data.read())
            for tag in tags:
                Tag.objects.get_or_create(**tag)
