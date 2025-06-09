from django.db import models
from django.contrib.auth.models import User

class UserData(models.Model):
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=10, blank=True, null=True)
    last_name = models.CharField(max_length=10, blank=True, null=True)
    email = models.CharField(max_length=100)
    phone_number = models.IntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    pin_code = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return self.first_name

class ProductModel(models.Model):
    item_image = models.ImageField(upload_to='item_image/')
    item_name = models.CharField(max_length=80)
    item_total = models.IntegerField()
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    item_brand = models.CharField(max_length=80)
    item_color = models.CharField(max_length=80, default='')
    is_bestSeller = models.BooleanField(default=False)
    is_newArrival = models.BooleanField(default=False)
    is_size6 = models.BooleanField(default=False)
    is_size7 = models.BooleanField(default=False)
    is_size8 = models.BooleanField(default=False)
    is_size9 = models.BooleanField(default=False)
    is_size10 = models.BooleanField(default=False)
    discount = models.IntegerField(default=0)


class CartModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    item_quantity = models.IntegerField()
    item_size = models.IntegerField(default=7)

class WishlistModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(ProductModel, on_delete=models.CASCADE)

class UserProductModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(ProductModel, on_delete=models.CASCADE)

class SideImage(models.Model):
    item_image = models.ImageField(upload_to='side_image/')
    item_name = models.CharField(max_length=80)
    item = models.ForeignKey(ProductModel, on_delete=models.CASCADE)

class ItemVariant(models.Model):
    item_image = models.ImageField(upload_to='item_variants/')
    item_name = models.CharField(max_length=80)
    item = models.ForeignKey(ProductModel, on_delete=models.CASCADE)



class PurchaseHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=False)
    order_id = models.TextField(max_length=80)
    payment_id = models.TextField(max_length=80)
    amount = models.IntegerField()
    email = models.EmailField()
    purchase_date = models.DateField()