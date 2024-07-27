from django.contrib import admin

from .models import Post, Comment




@admin.action(description='to upper title')
def to_upper(modeladmin, request, queryset):
    for obj in queryset:
        obj.title=obj.title.upper()
        obj.save()


@admin.action(description='to lower title')
def to_lower(modeladmin, request, queryset):
    for obj in queryset:
        obj.title=obj.title.lower()
        obj.save()
    
    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=('title','autor','status')
    search_fields=('title','autor')
    list_filter=('updated',)
    prepopulated_fields={'slug':('body','autor')}
    actions=[to_upper,to_lower]
    date_hierarchy='created'

@admin.register(Comment)
class commentAdmin(admin.ModelAdmin):
    list_display=('name', 'post', 'updated', 'active')
    list_filter=('name','active')
    search_fields=['name','email','body']
    









