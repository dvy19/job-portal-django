from django.urls import path

from .views import CommentView, JobView, LikeToggleView, PostDetailView

urlpatterns = [
   
    path('recruiter/create_job/', JobView.as_view()),

    path('posts/<int:post_id>/', PostDetailView.as_view()),

    path('posts/<int:post_id>/comments/', CommentView.as_view()),

    path('posts/<int:post_id>/like/', LikeToggleView.as_view()),

]

