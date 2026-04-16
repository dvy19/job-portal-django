from django.urls import path

from .views import  BlogDeleteView, BlogView, JobView
urlpatterns = [
   
    path('recruiter/create_job/', JobView.as_view()),



    path('create_blogs/', BlogView.as_view()),

    path("delete_blog/<int:pk>/", BlogDeleteView.as_view(), name="delete-blog"),



]

