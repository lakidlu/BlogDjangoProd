from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class Summary(models.Model):
    timestamp = models.CharField(unique=True, max_length=255, null=False)
    czas = models.DateTimeField(default=timezone.now(), null=False)
    status = models.IntegerField(null=False)
    wodne = models.IntegerField(null=False)
    wiatrowe = models.IntegerField(null=False)
    PV = models.IntegerField(null=False)
    generacja = models.IntegerField(null=False)
    zapotrzebowanie = models.IntegerField(null=False)
    czestotliwosc = models.FloatField(null=False)
    inne = models.IntegerField(null=False)
    cieplne = models.IntegerField(null=False)

    def __str__(self):
        return self.timestamp


class Connections(models.Model):
    timestamp_id = models.CharField(unique=True, max_length=255, null=False)
    timestamp = models.CharField(max_length=255, null=False)
    czas = models.DateTimeField(default=timezone.now(), null=False)
    status = models.IntegerField(null=False)
    ID = models.CharField(max_length=5, null=False)
    wartosc = models.IntegerField(null=False)
    rownolegly = models.IntegerField(null=False)
    wartosc_plan = models.IntegerField(null=False)

    def __str__(self):
        return self.timestamp

    def __repr__(self):
        return self.ID


class Exchanges(models.Model):
    timestamp = models.CharField(unique=True, max_length=255, null=False)
    status = models.IntegerField(null=False)
    czas = models.DateTimeField(default=timezone.now(), null=False)
    eksport = models.IntegerField(null=False)
    importt = models.IntegerField(null=False)
    saldo = models.IntegerField(null=False)

    def __str__(self):
        return self.timestamp


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                     self).get_queryset()\
                          .filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    object = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)

    def get_absolute_url(self):
        return reverse('blog:post_details',
                       args=[self.publish.year,
                             self.publish.strftime('%m'),
                             self.publish.strftime('%d'),
                             self.slug])

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Komentarz dodany przez {} dla posta {}'.format(self.name, self.post)
