from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from blog.models import Article

User = get_user_model()

# Create your models here.

class Comment(models.Model):
    author      = models.ForeignKey(User,on_delete=models.CASCADE)
    article     = models.ForeignKey(Article,on_delete=models.CASCADE)
    content     = models.TextField(null=False,blank=False)
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
