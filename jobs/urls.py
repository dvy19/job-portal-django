from django.urls import path

from .views import BlogView, CommentView, JobView, LikeToggleView, PostDetailView, PostView

urlpatterns = [
   
    path('recruiter/create_job/', JobView.as_view()),

    path('recruiter/create_post/', PostView.as_view()),

    path('create_blogs/', BlogView.as_view()),

    path('posts/<int:post_id>/', PostDetailView.as_view()),

    path('posts/<int:post_id>/comments/', CommentView.as_view()),

    path('posts/<int:post_id>/like/', LikeToggleView.as_view()),

]

