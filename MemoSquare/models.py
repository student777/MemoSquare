from django.db import models
from django.contrib.auth.models import User


class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    img_url = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username


class Page(models.Model):
    url = models.CharField(max_length=255)

    def __str__(self):
        return self.url


class Memo(models.Model):
    content = models.TextField()
    owner = models.ForeignKey(User, related_name='memo', on_delete=models.CASCADE)
    page = models.ForeignKey('Page', related_name='memo', on_delete=models.CASCADE)
    clipper = models.ManyToManyField(User, related_name='clipper', blank=True)
    is_private = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        content_truncated = self.content[:100] + (self.content[100:] and '..')
        return self.owner.__str__() + "/" + content_truncated


