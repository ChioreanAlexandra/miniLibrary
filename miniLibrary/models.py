from django.db import models
from django.urls import reverse
from django import forms

from django.contrib.auth.models import User
# Create your models here.

class Book(models.Model):
    name = models.CharField(max_length = 255)
    author = models.CharField(max_length = 150)
    description = models.TextField()
    publisher = models.CharField(max_length = 50)
    price = models.FloatField()
    def get_absolute_url(self):
        return reverse('book-detail', args=[self.id])
    def __str__(self):
        infos="%s %s %f "%(self.name, self.author, self.price)
        return infos
    @property
    def has_image(self):
         if Image.objects.get(book_id=self):
             return True
         else:
            return False
    def getBookWithId(id):
        qs=Book.objects.get(id=id);
        if qs:
            return qs
        return None
    @property
    def book_image(self):
        return Image.objects.get(book_id=self).name.url

  
class User(models.Model):
    username = models.CharField(max_length = 255)
    password =  models.CharField(max_length = 255)
    role =  models.CharField(max_length = 255, default = "client")
    def __str__(self):
        infos="%s %s %s"%(self.username, self.password, self.role)
        return infos


class Order(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    bookId = models.ForeignKey(Book, on_delete=models.CASCADE)
    placement_date = models.DateTimeField()
    def __str__(self):
        infos="%s %s %s"%(self.userId, self.bookId, self.placement_date)
        return infos

class Image(models.Model):
     name = models.ImageField(upload_to='images/')
     book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
