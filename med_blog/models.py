from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name



class Post(models.Model):
    title = models.CharField(max_length=75)
    body = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title










