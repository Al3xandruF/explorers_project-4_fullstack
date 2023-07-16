from django.urls import path
from . import views

urlpatterns = [
    path('', viewws.index, name="index")
    path('post/<slug:slug>', views.post_page, name='post_page')
]
