from ..models import Post
from django import template
from django.db.models import Count


register=template.Library()

@register.simple_tag
def total_posts():
    return Post.published.all().count()


@register.inclusion_tag('blog/last_post.html')
def show_lasted_posts():
    lasted_posts=Post.published.all().order_by('-publish')[:3]
    return {
        'lasted_posts':lasted_posts
    }


@register.inclusion_tag('blog/most_com.html')
def get_most_comment():
    most_comment=Post.published.annotate(total_comment=Count('post_comments')).order_by('-total_comment')[:3]
    return {
        'most_comment':most_comment,
    }
