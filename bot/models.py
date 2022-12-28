from django.db import models
from PIL import ImageFile


class ProductList(models.Model):
    product_name = models.CharField('Product_name',max_length=100)
    description = models.TextField('Description')
    price = models.FloatField('Price')
    image = models.ImageField('Image')
    status = models.BooleanField('Status')

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"



