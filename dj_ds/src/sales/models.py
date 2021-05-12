from django.db import models
from django.db.models import CASCADE
from customers.models import Customer
from profiles.models import Profile
from products.models import Product
from django.utils import timezone
from .utils import generate_code
from django.shortcuts import reverse

# Create your models here.\
class Position(models.Model):
    product = models.ForeignKey(Product, on_delete=CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField(blank=True)
    #Leave created date time as blank so we can modify in admin page
    created = models.DateTimeField(blank=True)

    def save(self, *args,**kwargs):
        self.price = self.product.price * self.quantity
        return super().save(*args,**kwargs)
    def __str__(self):
        return f"id: {self.id}, product: {self.product.name}, quantity: {self.quantity} "

    #perform a reverse relationship


        #sale_object = self.sale_set.first()
        #return sale_object.transaction_id
    def get_sales_id(self):
        sale_object = self.sale_set.first()
        return sale_object.id






class Sale(models.Model):
    transaction_id = models.CharField(max_length=12, blank=True)
    positions = models.ManyToManyField(Position)
    total_price = models.FloatField(blank=True, null=True)
    customers = models.ForeignKey(Customer, on_delete=CASCADE)
    salesman = models.ForeignKey(Profile, on_delete=CASCADE)
    created = models.DateTimeField(blank= True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.pk} : Sales for the amount of ${self.total_price}"


    def get_absolute_url(self):
        return reverse('sales:detail',kwargs={'pk':self.pk})

    def save(self,*args,**kwargs):
        if self.transaction_id =="":
            self.transaction_id = generate_code()
        if self.created == None:
            self.created = timezone.now()
        return super().save(*args, **kwargs)

    def get_positions(self):
        return self.positions.all()

    def get_trans_id(self):
        return self.transaction_id



class CSV(models.Model):
    file_name = models.FileField(upload_to='csvs')
    activated = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.file_name)
