from django.db import models
from django.urls import reverse
from accounts.models import User



class Category(models.Model):
    name=models.CharField(max_length=200)
    slug=models.SlugField(max_length=200,unique=True)

    class Meta:
        ordering=('name',)
        verbose_name='دسته بندی'
        verbose_name_plural='دسته بندی ها'

    def __str__(self):
        return self.name    


class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')
    name=models.CharField(max_length=300)
    slug=models.SlugField(max_length=250,unique=True)
    image=models.ImageField(upload_to='products/')
    description=models.TextField()
    price=models.IntegerField()
    available=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=('name',)
        verbose_name='محصول  '
        verbose_name_plural=' محصولات'
        

    def __str__(self):
        return self.name 
        
    def get_absolute_url(self):
        return reverse('shop:product_detail',args=[self.slug,])



class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='orders')
    paid=models.BooleanField(default=False)
    created=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now=True)

    class Meta:
        ordering=('paid','-updated')
        verbose_name='سفارش  '
        verbose_name_plural=' سفارش ها'
    def __str__(self):
        return f'{self.user} - {str(self.id)}'   

    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())          

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    price=models.IntegerField()
    quantity=models.IntegerField(default=1)

    def __str__(self):
        return str(self.id)
        
    def get_cost(self):
        return self.price*self.quantity



