from django.contrib import admin
from bot.models import ProductList
from faker import Faker

@admin.register(ProductList)
class ProductListAdmin(admin.ModelAdmin):
    ...
    '''fake = Faker("en_US")
    for _ in range(200):
        product_name = fake.name()
        description = fake.text()
        price = fake.random.randint(0,100000)
        status = fake.boolean()
        image = "stock-photo-closeup-of-vinyl-long-play.jpg"
        data = ProductList(product_name = product_name, description = description, price = price, status = status, image = image)
        data.save()'''
    
  

