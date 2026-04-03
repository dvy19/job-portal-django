from django.urls import path

from views import JobView

urlpatterns = [
    
    path('recruiter/create_job/', JobView.as_view())


]