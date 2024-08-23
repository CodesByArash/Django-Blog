from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid

# Create your models here.

User = get_user_model()

class Category(models.Model):
    id          = models.UUIDField(primary_key = True, default= uuid.uuid4, editable = False)
    name        = models.CharField(max_length = 50, blank = False, null = False, unique = True)
    description = models.CharField(max_length = 200, blank = False, null = False,)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.description:
            self.description = self.name
        super(Category, self).save(*args, **kwargs)


class Article(models.Model):
    id          = models.UUIDField(primary_key = True, default= uuid.uuid4, editable = False)
    title       = models.CharField(max_length = 50, blank = False, null = False)       
    slug        = models.SlugField(max_length=50, blank = False, null = False, unique = True )
    author      = models.ForeignKey(User,on_delete=models.CASCADE)
    content     = models.TextField(null=False,blank=False)
    publish     = models.DateTimeField(default = timezone.now)
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    status      = models.BooleanField(default=False)
    categories  = models.ManyToManyField('Category', related_name='articles', blank= True, symmetrical=False)

    def __str__(self):
        return self.title
    
    
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name='ratings', on_delete=models.CASCADE)
    score = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
