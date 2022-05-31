
from multiprocessing import context
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views import View
from .models import Post
from .forms import CommentForm
# def get_date(post):
#     return post['date']

# Create your views here.

# class view of starting page
class StartingPageView(ListView):
    template_name = 'myapp/index.html'
    model = Post
    ordering = ["-date"]
    context_object_name = 'posts'

    def get_queryset(self):
        

        query_set =  super().get_queryset()
        data = query_set[:3]
        return data

# all posts view
class AllPostsView(ListView):
    template_name = 'myapp/all-posts.html'
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"

# single post class view
class SinglePostView(View):

    def is_stored_posts(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False
        
        return is_saved_for_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        
        context={
            "post":post, 
            "post_tags":post.tags.all(),
            "comment_form":CommentForm(),
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_posts(request, post.id)
        }
        return render(request, 'myapp/post-detail.html', context )

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        # if form is valid
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('single-post-page', args=[slug]))
        
        # if form is invlid
        
        context={
            "post":post, 
            "post_tags":post.tags.all(),
            "comment_form":CommentForm(),
            "comments": post.comments.all().order_by("-id"),
             "saved_for_later": self.is_stored_posts(request, post.id)
        }
        
        return render(request, 'myapp/post-detail.html', context)
        
class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")
        context = {}

        if stored_posts is None or len(stored_posts)==0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in = stored_posts)
            context["posts"] = posts
            context["has_posts"] = True
        
        return render(request, "myapp/stored_posts.html", context)

    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []
        
        post_id = int(request.POST["post_id"])
        
        if post_id not in stored_posts:

            stored_posts.append(post_id)
            request.session["stored_posts"] = stored_posts
        else:
            stored_posts.remove(post_id)
        
        request.session["stored_posts"] = stored_posts
        
        return HttpResponseRedirect("/")

def search_blogs(request):
        if 'q' in request.GET:
            q=request.GET['q']
            posts = Post.objects.filter(title__icontains=q)
        else:
            posts = Post.objects.all()
        
        return render(request, 'myapp/index.html', {"posts":posts})