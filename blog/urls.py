from django.urls import path
from blog.views import ListPostview,DetailPostview,SharePostView
from .feeds import LastedPostFeed

app_name='blog'


urlpatterns=[
    path('<slug:tag_name>/',ListPostview.as_view(), name='main_tag'),
    path('',ListPostview.as_view(), name='main'),
    path('detail/<int:year>/<int:month>/<int:day>/<slug:slug>',DetailPostview.as_view(), name='detail_page'),
    path('share/<int:post_id>/',SharePostView.as_view(), name='share_post'),
    path('feed/', LastedPostFeed(), name='post_feed'),
]

