from django.shortcuts import render
from psycopg2 import IntegrityError
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Create your views here.
from django.shortcuts import get_object_or_404

from .models import Blog, Job, JobApplication
from .serializers import BlogSerializer, JobApplicationSerializer
from rest_framework import status
from .serializers import JobSerializer

from rest_framework.pagination import PageNumberPagination

class JobPagination(PageNumberPagination):
    page_size = 10


class BlogDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            blog = Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check ownership
        if blog.user != request.user.recruiterprofile:
            return Response({"error": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

        blog.delete()
        return Response({"message": "Blog deleted successfully"}, status=status.HTTP_200_OK)

class JobView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = JobSerializer(data=request.data)

        if serializer.is_valid():
            job = serializer.save(user=request.user.recruiterprofile)

            response_serializer = JobSerializer(job)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None):

        # 🔹 CASE 1: Get single job
        if id is not None:
            job = get_object_or_404(Job, id=id)
            serializer = JobSerializer(job)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # 🔹 CASE 2: Get all jobs (your existing logic)
        jobs = Job.objects.all().order_by('-created_at')

        paginator = JobPagination()
        paginated_jobs = paginator.paginate_queryset(jobs, request)

        serializer = JobSerializer(paginated_jobs, many=True)
        return paginator.get_paginated_response(serializer.data)
    
class BlogView(APIView):

    permission_classes=[IsAuthenticated]

    def post(self,request):
        serializer=BlogSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user.recruiterprofile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
    def get(self,request):
        blogs=Blog.objects.all().order_by('-created_at')
        serializer=BlogSerializer(blogs,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ApplyJobView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        job_id = request.data.get("job")

        # ❗ Check job exists
        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response(
                {"error": "Job not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # ❗ Get logged-in job seeker
        try:
            applicant = request.user.jobseekerprofile
        except:
            return Response(
                {"error": "Only job seekers can apply"},
                status=status.HTTP_403_FORBIDDEN
            )

        # ❗ Prevent duplicate application
        if JobApplication.objects.filter(job=job, applicant=applicant).exists():
            return Response(
                {"error": "You have already applied for this job"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ Create application
        application = JobApplication.objects.create(
            job=job,
            applicant=applicant
        )

        serializer = JobApplicationSerializer(application)

        return Response(serializer.data, status=status.HTTP_201_CREATED)