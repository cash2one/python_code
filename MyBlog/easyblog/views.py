from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from easyblog.models import BlogPost


def index(request):
    blog_list = BlogPost.objects.all()
    return render(request, 'index.html', {'blog_list': blog_list})
