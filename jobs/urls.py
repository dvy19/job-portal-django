from django.urls import path

from .views import  ApplyJobView, BlogDeleteView, BlogView, JobView
urlpatterns = [
   
    path('recruiter/create_job/', JobView.as_view()),
    path('jobs/<int:id>/', JobView.as_view()), # detail



    path('create_blogs/', BlogView.as_view()),

    path("delete_blog/<int:pk>/", BlogDeleteView.as_view(), name="delete-blog"),
    
    path('apply/', ApplyJobView.as_view(), name='apply-job'),


]

