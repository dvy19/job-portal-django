from django.urls import path
from .views import JobRecruiterProfileView, JobSeekerProfileView, LoginView, RegisterView, SkillView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', JobSeekerProfileView.as_view()),
    path('recruiter-profile/', JobRecruiterProfileView.as_view()),


    path('skills/', SkillView.as_view()),   # 🔥 separate skill endpoint

]

'''

{
    "name":"Kotlin App Development"
}


{
    "message": "Skill created successfully",
    "data": {
        "id": 3,
        "name": "Kotlin App Development"
    }
}
'''