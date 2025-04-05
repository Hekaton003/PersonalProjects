from django.urls import path
from .views import PostListView,PostDetailView,PostCreateView,PostUpdateView,PostDeleteView,UserPostListView
from . import views

urlpatterns = [
    path('hello/', views.say_hello,name='firstApp-hello'),
    path('',PostListView.as_view(),name='firstApp-home'),
    path('about/', views.about,name='firstApp-about'),
    path('post/new',PostCreateView.as_view(),name='firstApp-post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='firstApp-post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='firstApp-post-delete'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='firstApp-post-detail'),
    path('user/<str:username>', UserPostListView.as_view(), name='firstApp-user-posts'),
]
