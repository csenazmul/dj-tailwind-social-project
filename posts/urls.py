from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.PostCreateView.as_view(), name='create_post'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='edit_post'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='delete_post'),
    path('profile/', views.profile_view, name='profile'),
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
]
