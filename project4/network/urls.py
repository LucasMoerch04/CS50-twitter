
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newPost", views.new_post_view, name="new_post"),
    path("profile/<int:profile_id>", views.profile_page_view, name="profile"),
    path("edit_follow/<int:profile_id>", views.follow, name="edit_follow"),
    path("following", views.following_view, name="following"),
    path("edit_post", views.edit_post, name="edit_post"),
    path("like_post", views.like_post, name="like_post"),
    path("changePfp", views.changePfp, name="changePfp")

    
]
