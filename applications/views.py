from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import JobApplication, JobSeekerProfile, Job


class ApplyJobView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, job_id):
        job = get_object_or_404(Job, id=job_id)
        seeker = JobSeekerProfile.objects.get(user=request.user)

        # Prevent duplicate application
        if JobApplication.objects.filter(job=job, seeker=seeker).exists():
            return Response({"message": "Already applied"}, status=400)

        application = JobApplication.objects.create(
            job=job,
            seeker=seeker
        )

        return Response({
            "message": "Applied successfully"
        })