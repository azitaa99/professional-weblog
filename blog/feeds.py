from django.contrib.syndication.views import Feed
from django.db.models.base import Model
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from django.utils.safestring import SafeText
from .models import Post



class LastedPostFeed(Feed):
    title='my blog'
    link=reverse_lazy('blog:main')
    description='new post of my blog'

    def items(self):
        return Post.published.all()[:5]
    

    def item_title(self, item):
        return item.title
    
    def item_description(self, item: Model) -> str:
        return truncatewords(item.body,30)