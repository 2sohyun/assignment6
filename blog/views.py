from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import BlogForm, CommentForm, HashtagForm
from .models import Blog, Comment, Hashtag
# Create your views here.

# Read
def home(request):
    blogs = Blog.objects
    hashtags = Hashtag.objects
    return render(request, 'blog/home.html', {'blogs': blogs, 'hashtags': hashtags})

# Create
def blogform(request, blog=None):       
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.pub_date = timezone.now()
            blog.save()
            form.save_m2m()
            return redirect('home')
    else:
        form = BlogForm(instance=blog)
        return render(request, 'blog/new.html', {'form': form})

# Edit
def edit(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    return blogform(request, blog)

# Delete
def remove(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    blog.delete()
    return redirect('home')

#댓글생성
def detail(request, blog_id, comment=None):
        blog = get_object_or_404(Blog, id = blog_id)
        if request.method == "POST":
                form = CommentForm(request.POST, instance=comment)
                if form.is_valid():
                        comment = form.save(commit=False)
                        comment.blog = blog
                        comment.comment_text = form.cleaned_data["comment_text"]
                        comment.save()
                        return redirect("home")

        else:
                form = CommentForm(instance=comment)
                return render(request, "blog/detail.html", {"blog":blog, "form":form})

def comment_edit(request, blog_id, pk):
        comment = get_object_or_404(Comment, pk=pk)
        return detail(request, blog_id, comment)

def comment_remove(request, blog_id, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return redirect('home')

def hashtagform(request, hashtag=None):
        if request.method == 'POST':
                form = HashtagForm(request.POST, instance=hashtag)
                if form.is_valid():
                        hashtag = form.save(commit=False)
                        if Hashtag.objects.filter(name=form.cleaned_data['name']):
                                form = HashtagForm()
                                error_message = "♨이미 존재하는 해시태그입니당♨"
                                return render(request, 'blog/hashtag.html', {'form':form, "error_message":error_message})
                        else:
                                hashtag.name = form.cleaned_data['name']
                                hashtag.save()
                                return redirect('home')
        else:
                form = HashtagForm(instance=hashtag)
                return render(request, 'blog/hashtag.html', {'form':form})

def search(request, hashtag_id):
        hashtag = get_object_or_404(Hashtag, pk=hashtag_id)
        return render(request, 'blog/search.html', {'hashtag': hashtag})