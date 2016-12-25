from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import slugify

from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    
    def __str__(self):
        return self.user.username

class Category(models.Model):
    MAX_LENGTH = 128
    name = models.CharField(max_length=MAX_LENGTH, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if self.views < 0:
            self.views = 0
        
        super(Category, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name
    
class Page(models.Model):
    MAX_LENGTH=128
    
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=MAX_LENGTH)
    url = models.TextField()
    views = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
    
    def __unicode__(self):
        return self.title




