from django.shortcuts import render
from psycopg2 import IntegrityError
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Create your views here.

from .models import Blog, Job
from .serializers import BlogSerializer
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

    permission_classes=[IsAuthenticated]

    def post(self,request):
        serializer=JobSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user.recruiterprofile)
            return Response( serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
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


    permission_classes = [IsAuthenticated]

    def post(self, request, job_id):
        user = request.user

        # ✅ Get Job
        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response({"error": "Job not found"}, status=404)

        # ✅ Safe Create (handles duplicate apply)
        try:
            application = JobApplication.objects.create(user=user, job=job)
        except IntegrityError:
            return Response({"error": "You already applied to this job"}, status=400)

        serializer = JobApplicationSerializer(application)
        return Response(serializer.data, status=201)
    
    