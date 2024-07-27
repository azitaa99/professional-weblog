from django.contrib.sitemaps import  Sitemap
from django.db.models.base import Model
from .models import Post




class postsitemap(Sitemap):
    changefreq='never'
    priority=0.9
    def items(self):
        return Post.published.all()
    


    
    


