from django import forms
from .models import Comment




class PostForm(forms.Form):
    name=forms.CharField(max_length=100)
    email=forms.EmailField()
    to=forms.EmailField()
    comment=forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['name','email','body']
        widgets={
            'body':forms.Textarea
        }


class SearchForm(forms.Form):
    query=forms.CharField()


class shForm(forms.Form):
    query=forms.CharField()