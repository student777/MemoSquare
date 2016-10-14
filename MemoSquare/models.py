from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    img_url = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserDetail.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userdetail.save()


class Page(models.Model):
    url = models.CharField(max_length=255)

    def __str__(self):
        return self.url


class Memo(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    owner = models.ForeignKey(User, related_name='memo', on_delete=models.CASCADE)
    page = models.ForeignKey('Page', related_name='memo', on_delete=models.CASCADE)
    dom_location = models.CharField(max_length=25)
    is_private = models.BooleanField()

    def __str__(self):
        return self.title + "/" + self.owner.__str__()
