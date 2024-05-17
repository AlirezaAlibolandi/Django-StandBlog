from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.name

class Tag(models.Model):
    title = models.CharField(max_length=100,unique=True,null=True)
    def __str__(self):
        return self.title

class Articles(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles_related')
    title = models.CharField(max_length=150)
    body = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    images = models.ImageField(upload_to='images/articles')
    slug = models.SlugField(null=True,unique=True,blank=True,max_length=250)

    # class Meta:
    #     ordering = ['-pub_date'],
    #     verbose_name_plural = 'articles',
    #     get_latest_by = 'pub_date',
    #     verbose_name = 'article'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('Details:details' , args=[self.id])

    def __str__(self):
        return self.title


class comments(models.Model):
    article = models.ForeignKey(Articles, on_delete=models.CASCADE, related_name='articles_comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='articles_comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True,blank=True)
    comment = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return self.comment[:100]


class Likes(models.Model):
    article = models.ForeignKey(Articles, on_delete=models.CASCADE, related_name='articles_likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_likes')
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ('-created',)