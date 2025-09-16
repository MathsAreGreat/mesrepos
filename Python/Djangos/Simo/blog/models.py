from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your models here.

User = get_user_model()  # supports custom user models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=200, default="")
    content = models.TextField()
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="posts", default=1)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_created")
