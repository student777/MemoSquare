from django.db import models
from django.contrib.auth.models import User


class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    provider = models.CharField(max_length=20, blank=True)
    code = models.CharField(max_length=100, blank=True)
    img_url = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username


class Page(models.Model):
    url = models.CharField(max_length=255)

    def __str__(self):
        return self.url


class Memo(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    user = models.ForeignKey(User, related_name='memo', on_delete=models.CASCADE)
    page = models.ForeignKey('Page', related_name='memo', on_delete=models.CASCADE)
    dom_location = models.CharField(max_length=25)
    is_private = models.BooleanField()

    def __str__(self):
        return self.title + "/" + self.user.__str__()
