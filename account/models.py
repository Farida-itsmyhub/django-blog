from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    register_people = PublishedManager()
    objects = models.Manager()

    def __str__(self):
        return 'Profile for users {}'.format(self.user.username)


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post')
    image = models.ImageField(upload_to='posts/%Y/%m/%d/', blank=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250, allow_unicode=True, unique_for_date='publish')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Created on {}'.format(self.created)

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)  # скрыть некоторые комменты

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comments by {} on {}'.format(self.name, self.post)

    def get_photo(self):
        users = Profile.objects.all()
        return users.filter(user=self.name)
