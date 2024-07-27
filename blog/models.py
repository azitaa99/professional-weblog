from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

from taggit.managers import TaggableManager




class PublishManager(models.Manager):
    def get_queryset(self):
        return super(PublishManager,self).get_queryset().filter(status='publish')



class Post(models.Model):
    STATUS_CHOICES=(('draft','Draft'),('publish','Publish'),)
    title=models.CharField(max_length=200)
    slug=models.CharField(max_length=250,unique_for_date='publish')
    autor=models.ForeignKey(User,on_delete=models.CASCADE, related_name='posts')
    body=models.TextField(max_length=5000)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    publish=models.DateTimeField(default=timezone.now)
    status=models.CharField(max_length=100, choices=STATUS_CHOICES , default='draft')
    tags = TaggableManager(blank=True)


    objects=models.Manager()
    published=PublishManager()

    def __str__(self) -> str:
        return(f'{self.title}')
    
    def get_absolute_url(self):
        return reverse('blog:detail_page',args=[self.publish.year,
                                                self.publish.month,
                                                self.publish.day,
                                                self.slug])
    



class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE, related_name='post_comments')
    name=models.CharField(max_length=150)
    email=models.EmailField()
    body=models.CharField(max_length=500)
    active=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    
    

    class Meta:
        ordering=('created',)
    
    def __str__(self):
        return f'{self.email} commented for {self.post}'



