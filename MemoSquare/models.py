from django.db import models
from django.contrib.auth.models import User


class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='detail')
    provider = models.CharField(max_length=10)  # i hate foreign key...
    img_url = models.CharField(max_length=255)  # this has to be created because of fuck google

    def __str__(self):
        return self.user.get_full_name()


class Page(models.Model):
    url = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.url


class Category(models.Model):
    # Need for sub primary key starting from 1 for each user
    name = models.CharField(max_length=45)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'user')

    def __str__(self):
        return self.name


class Memo(models.Model):
    title = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    clips = models.ManyToManyField(User, through='Clip', related_name='+')
    likes = models.ManyToManyField(User, through='LikeMemo', related_name='+')
    is_private = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        content_truncated = self.content[:100] + (self.content[100:] and '..')
        return self.user.__str__() + "/" + content_truncated


class Clip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    memo = models.ForeignKey(Memo, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + '/' + self.memo.title

    class Meta:
        unique_together = ('user', 'memo')


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.user.username + '/' + self.content[:30]


class Comment(models.Model):
    content = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    memo = models.ForeignKey(Memo, on_delete=models.CASCADE, related_name='comment')
    likes = models.ManyToManyField(User, through='LikeComment', related_name='+')
    timestamp = models.DateTimeField(auto_now_add=True)


class LikeMemo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    memo = models.ForeignKey(Memo, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'memo')


class LikeComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'comment')
