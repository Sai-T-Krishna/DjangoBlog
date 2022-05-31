from django.urls import path, include

from . import views 

urlpatterns = [
    path("", views.StartingPageView.as_view(), name="starting-page"),
    path("posts/", views.AllPostsView.as_view(), name="posts-page"),
    path("posts/<slug:slug>", views.SinglePostView.as_view(), name="single-post-page") , # /posts/my-first-post
    path("read-later", views.ReadLaterView.as_view(), name="read-later"),
    path("search-blogs",views.search_blogs, name ='search_blogs')
    
]
