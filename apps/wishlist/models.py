from __future__ import unicode_literals
from django.db import models
from ..loginreg.models import User

class ProductManager(models.Manager):
    def productValidate(self, data):
        errors = []

        if len(data['product_name']) == 0:
            errors.append("Item/product name cannot be blank. Please check and re-submit.")
        if len(data['product_name']) < 3:
            errors.append("Item/Product name cannot be less than 3 characters.")

        if len(errors) != 0:
            return {'errors' : errors}

        user = User.objects.get(id=data['id'])
        product = Product.objects.create(product_name = data['product_name'], creator=user)
        product.users.add(user)
        return {'product' : product}

class Product(models.Model):
    product_name = models.CharField(max_length = 249)
    users = models.ManyToManyField(User, related_name="wishes")
    creator = models.ForeignKey(User, related_name="created_wishes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProductManager()
