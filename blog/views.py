from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Blogpost 

# Create your views here.
def index(request):
    blogs = Blogpost.objects.all()
    # blogs_content = []
    # for blog in blogs:
    #     blog_list = [blog.title,blog.head0,blog.chead1,blog.head1,blog.chead1]
    #     blogs_content.append(blog_list)

    blogs_dict={'blogs_content':blogs}     
    return render(request, 'blog/index.html',blogs_dict)
def blogpost(request,id):
    blogs = Blogpost.objects.filter(Post_id=id)[0]
    return render(request, 'blog/blogpost.html',{'blogs':blogs})