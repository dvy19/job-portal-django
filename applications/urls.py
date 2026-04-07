from django.urls import path

from .views import ApplyJobView

urlpatterns = [
   
    path('apply-job/<int:job_id>/', ApplyJobView.as_view()),

]

