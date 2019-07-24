from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Post,Category
# Create your views here.



class PostList(ListView):
    model = Post
    template_name = 'med_blog/post_list.html'
    context_object_name = 'posts'


class PostDetail(DetailView):
    model = Post
    template_name = 'med_blog/post_detail.html'
    context_object_name = 'post'


class CategoryDetail(DetailView):
    model = Category
    template_name = 'med_blog/category_detail.html'
    context_object_name = 'category'