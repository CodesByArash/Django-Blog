from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
# Create your models here.

User = get_user_model()

class Category(models.Model):
    name        = models.CharField(max_length = 50, blank = False, null = False, unique = True)
    description = models.CharField 

class Article(models.Model):
    title       = models.CharField(max_length = 50, blank = False, null = False)       
    slug        = models.SlugField(max_length=50, blank = False, null = False, unique = True )
    author      = models.ForeignKey(User,on_delete=models.CASCADE)
    category    = models.ForeignKey(Category,on_delete=models.CASCADE)
    content     = models.TextField(null=False,blank=False)
    # publish     = models.DateTimeField(default = timezone.now)
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    status      = models.BooleanField(default=False)

    def __str__(self):
        return self.title