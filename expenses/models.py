from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
# Create your models here.

class Expense(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    owner = models.ForeignKey(to=User , on_delete=models.CASCADE)
    description = models.TextField()
    category = models.CharField(max_length=100)  # Add category field

    def __str__(self):
        return self.category
    
    class Meta:
        ordering : [ '-date' ]  

    class Category(models.Model):
        name = models.CharField(max_length=100)