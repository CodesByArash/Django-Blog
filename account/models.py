from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils.translation import gettext_lazy as _




class User(AbstractUser):  
    id                = models.UUIDField(primary_key = True, default= uuid.uuid4, editable = False)
    username          = models.CharField(max_length = 50, blank = False, null = False, unique = True)  
    email             = models.EmailField(_('Email Address'), max_length=50, unique=True)
    is_email_verified = models.BooleanField(default=False)
    first_name        = models.CharField(default = "null", max_length=500, blank=True, null=True)
    last_name         = models.CharField(default = "null", max_length=500, blank=True, null=True)
    is_staff          = models.BooleanField(default=False, verbose_name='staff')
    bio               = models.TextField(blank=True, null = True, max_length=500)
    profile_img       = models.ImageField(upload_to='profile_images',default='/profile_images/default.png')
    posts             = models.IntegerField(default=0)
    

    REQUIRED_FIELDS = ['email', ]

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

