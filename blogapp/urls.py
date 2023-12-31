from . import views
from django.urls import path
from .views import handler404

urlpatterns = [
    path('', views.index, name="index"),
    path('post/<slug:slug>', views.post_page, name='post_page'),
    path('tag/<slug:slug>', views.tag_page, name='tag_page'),
    # path('author/<slug:slug>/', views.author_page, name='author_page'),
    path('about/', views.about, name='about'),
    path('accounts/register/', views.register_user, name='register'),
    path('update_comment/<int:pk>/', views.update_comment, name='update_comment'),  # noqa
    path('delete_comment/<int:pk>/', views.delete_comment, name='delete_comment'),  # noqa
    path('bookmark_post/<slug:slug>', views.bookmark_post, name='bookmark_post'),  # noqa
    path('like_post/<slug:slug>', views.like_post, name='like_post'),
    path('all_bookmarked_posts/', views.all_bookmarked_posts, name='all_bookmarked_posts'),  # noqa
    path('all_posts/', views.all_posts, name='all_posts'),
    path('all_liked_posts/', views.all_liked_posts, name='all_liked_posts')
]
