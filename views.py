from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import BlogPost
from .forms import BlogPostForm

# Create your views here.
def blogs(request):
    """Show all Blogs on the home page"""
    blogs = BlogPost.objects.order_by('created_on')
    context = {'blogs': blogs}
    return render(request, 'blogs/blogs.html', context)

@login_required
def new_blog(request):
    """Adding a new blog"""
    if request.method != 'POST':
        #No info submitted; create a blank form
        form = BlogPostForm
    else:
        #info submitted; process the new info
        form = BlogPostForm(data=request.POST)
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.owner = request.user
            new_blog.save()
            return redirect('blogs:blogs')

    context= {'form':form}
    return render(request, 'blogs/new_blog.html', context)

@login_required
def edit_blog(request, blog_id):
    """Editing a blog post"""
    blog = get_object_or_404(BlogPost, id=blog_id)
    check_blog_owner(request,blog.owner)

    if request.method != 'POST':
        #person clicks on the form- return current info
        form = BlogPostForm(instance=blog)
    else:
        #updating new information
        form= BlogPostForm(instance=blog, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:blogs')

    context = {'blog': blog, 'form':form}
    return render (request, 'blogs/edit_blog.html', context)

@login_required
def check_blog_owner(request,owner):
    """make sure correct owner for the blog post"""
    if owner != request.user:
        raise Http404

@login_required
def delete_blog(request,blog_id):
    """Deleting a blog"""
    blog = get_object_or_404(BlogPost, id=blog_id)
    check_blog_owner(request,blog.owner)

    if request.method == 'POST':
        blog.delete()
        return redirect('blogs:blogs')

    context = {'blog': blog}
    return render(request, 'blogs/delete_blog.html', context)
