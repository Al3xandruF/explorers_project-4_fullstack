from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('post/<slug:slug>', views.post_page, name='post_page'),
    path('tag/<slug:slug>', views.tag_page, name='tag_page'),
    path('author/<slug:slug>', views.author_page, name='author_page'),
    path('search/', views.search_posts, name='search'),
    path('about/', views.about, name='about'),
    path('accounts/register/', views.register_user, name='register'),
    path('update_comment/<int:pk>', views.update_comment, name='update_comment'),
    path('delete_comment/<int:pk>', views.delete_comment, name='delete_comment'),
]
