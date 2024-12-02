from django.urls import path
from posts import views

urlpatterns = [
    path('posts/', views.PostList.as_view()),  # class based view
    path('posts/<int:pk>/', views.PostDetail.as_view()),
]