from django.db import models
from django.urls import reverse
from django.conf import settings

# Create your models here.
ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)
class Category(models.Model):
    name = models.TextField(max_length=50,unique=True)
    slug = models.SlugField(max_length=50,unique=True,help_text='Unique calue for product page URL,created from name')    
    description= models.TextField()
    is_active= models.BooleanField(default=True)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['created_at']
    def get_absolute_url(self):
        return reverse("category", kwargs={"slug": self.slug})
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255,unique=True,help_text='Unique calue for product page URL,created from name')
    brand = models.CharField( max_length=50)
    price = models.DecimalField(max_digits=9,decimal_places=2)
    old_price = models.DecimalField(max_digits=9,decimal_places=2,blank=True,default=0.0)
    image=models.ImageField()
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ForeignKey(Category,on_delete=models.CASCADE,default="Clothes")
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['created_at']
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("homepage:product",kwargs={"slug": self.slug}) 
    def sale_price(self):
        if(self.old_price>self.price):
            return self.price
        else:
            return None
    def get_add_to_cart_url(self):
        return reverse("homepage:add-to-cart", kwargs={
            'slug': self.slug
        })
    def get_remove_from_cart_url(self):
        return reverse("homepage:remove-from-cart", kwargs={
            'slug': self.slug
        })    

class OrderProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} : {self.product.name}"

    def get_total_product_price(self):
        return self.quantity * self.product.price

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderProduct)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey('Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username
    def address_1(self):
        return self.shipping_address.street_address
    def address_2(self):
        return self.shipping_address.apartment_address

    def get_total(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.get_total_product_price()
        return total


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'





    
    


        


