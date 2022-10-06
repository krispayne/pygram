from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django import forms
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from posts.models import Post, Comment

class PostList(ListView):
    model = Post

class PostCreate(CreateView):
    model = Post
    fields = ['image', 'description']
    success_url = '/'

    def form_valid(self, form):
        Post = form.save(commit=False)
        Post.author = self.request.user
        Post.save()
        return super().form_valid(form)

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}))

class PostDetail(DetailView):
    model = Post

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = Comment(
                author=request.user,
                post=self.get_object(),
                text=comment_form.cleaned_data['comment']
            )
            comment.save()
        else:
            raise Exception
        return redirect(reverse('post-detail', args=[self.get_object().id]))