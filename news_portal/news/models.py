from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True)
    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="articles")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    tags = models.ManyToManyField(Tag, related_name="articles", blank=True)

    is_public = models.BooleanField(default=True, help_text="Should this article be published?")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title