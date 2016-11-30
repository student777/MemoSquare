from django.db import models
from django.contrib.auth.models import User


class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='detail')
    provider = models.CharField(max_length=10)  # i hate foreign key...
    img_url = models.CharField(max_length=100)  # this has to be created because of fuck google

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


class Page(models.Model):
    url = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.url


class Memo(models.Model):
    title = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    owner = models.ForeignKey(User, related_name='memo', on_delete=models.CASCADE)
    page = models.ForeignKey('Page', related_name='memo', on_delete=models.CASCADE)
    clipper = models.ManyToManyField(User, through='Clip', related_name='clipper')
    is_private = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        content_truncated = self.content[:100] + (self.content[100:] and '..')
        return self.owner.__str__() + "/" + content_truncated


class Clip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    memo = models.ForeignKey(Memo, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + '/' + self.memo.title


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.user.username + '/' + self.content[:30]