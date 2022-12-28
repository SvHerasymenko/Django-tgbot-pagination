import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tg_store.settings')

import django
django.setup()
from django.core.management.base import BaseCommand
from bot.models import ProductList

from django.core.paginator import Paginator

def get_id():
    count_id = ProductList.objects.all().filter(status = True)
    id = count_id.values_list("id", flat=True)
    return id

def get_description(id):
    products = ProductList.objects.get(id = id)
    description = products.description
    return description

def get_image(id):
    products = ProductList.objects.get(id = id)
    image = products.image
    return image
    
def get_price(id):
    products = ProductList.objects.get(id = id)
    price = products.price
    return price

def count_products():
    count_id = len(get_id())
    return count_id

def get_name(id):
    products = ProductList.objects.get(id = id)
    name = products.product_name
    return name