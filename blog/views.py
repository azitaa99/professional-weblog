from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import ListView,DetailView
from blog.models import Post, Comment
from django.views import View
from .forms import PostForm, CommentForm,SearchForm,shForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery,SearchRank


class ListPostview(View):
    form_class=shForm
    def get(self, request, tag_name=None):
        posts=Post.published.all().order_by('-publish')


        #search
        if request.GET.get('query'):
            form=self.form_class(request.GET)
            if form.is_valid():
                query=form.cleaned_data['query']
                search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
                search_query = SearchQuery(query)
                
                posts=Post.published.annotate(serachfield = search_vector,rank=SearchRank(search_vector,search_query)).filter(serachfield__contains = query).order_by('-rank')

       
            
        

        #tag
        if tag_name:
            tag = get_object_or_404(Tag, slug=tag_name)
            posts=Post.published.filter(tags__in=[tag])




        #pagination
        paginator = Paginator(posts, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        try:
            posts = paginator.page(page_number)
        except PageNotAnInteger: 
       
            posts = paginator.page(1)
        except EmptyPage:
      
            posts = paginator.page(paginator.num_pages)
        return render(request,
                     'blog/main.html',
                     {'page_obj': page_obj,
                     'posts': posts,
                     'tag_name':tag_name,
                     'form':self.form_class,
                     
                     })
        











class DetailPostview(View):
    form_class=CommentForm
    
    def get(self, request, year,month,day,slug):
        post=get_object_or_404(Post,slug=slug,status='publish',publish__year=year,publish__month=month,publish__day=day)
        comments=post.post_comments.all()

       #similar posts
        post_tags=post.tags.values_list('id',flat=True)
        similar_post=Post.published.filter(tags__in=post_tags).distinct().exclude(id=post.id)
        similar_post=similar_post.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')
        return render(request,'blog/detail.html',{'post':post,
                                                  'form':self.form_class,
                                                  'comments':comments,
                                                  'similar_post':similar_post})
     
    def post(self, request, year,month,day,slug):
        post=get_object_or_404(Post,slug=slug,status='publish',publish__year=year,publish__month=month,publish__day=day)
        comments=post.post_comments.all()
        form=self.form_class(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            new_comment=form.save(commit=False)
            new_comment.post=post
            new_comment.save()
            
        return redirect('blog:detail_page',year,month,day,slug)
        
        
    
    





    
class SharePostView(View):
    form_class=PostForm()
    sent=False
    def get(self, request, post_id):
        
        return render(request,'blog/share.html', {'form':self.form_class})

    def post(self, request,post_id):
        post=get_object_or_404(Post,id=post_id)
        form=self.form_class(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            post_url=request.build_absolute_uri(post.get_absolute_url())
            subject= f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"

        
            send_mail(subject,message,'azita@email.com',cd['to'])
            sent=True
        return redirect('blog:main')





    




# class searchview(View):
#     def get(self, request):
#         form = SearchForm()
#         # query = None
#         # posts=[]
#         # if request.GET.get('query'):
#         #     form = SearchForm(request.GET)
#         #     if form.is_valid():
#         #         query = form.cleaned_data['query']
#         #         search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
#         #         search_query = SearchQuery(query)
#         #         posts = Post.published.annotate(
#         #         rank=SearchRank(search_vector, search_query)
#         #         ).filter(rank__gte=0.3).order_by('-rank')

#         return render(request,'blog/search.html',{'form':form,
#                                                       })




    






    




