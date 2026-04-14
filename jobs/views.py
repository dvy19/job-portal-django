from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Create your views here.
from django.shortcuts import get_object_or_404

from .models import Blog, Job, Posts, Comment, Like
from .serializers import BlogSerializer, PostSerializer, CommentSerializer
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

# 🔥 Create + List Posts
class PostView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Posts.objects.all().order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(recruiter=request.user)
            return Response(serializer.data)
        return Response(serializer.errors)



# 🔥 Single Post
class PostDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        post = get_object_or_404(Posts, id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 💬 Comment View
class CommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Posts, id=post_id)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, post_id):
        post = get_object_or_404(Posts, id=post_id)
        comments = post.comments.all().order_by('-created_at')

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ❤️ Like Toggle
class LikeToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Posts, id=post_id)
        user = request.user

        like, created = Like.objects.get_or_create(user=user, post=post)

        if not created:
            like.delete()
            return Response({"liked": False}, status=status.HTTP_200_OK)

        return Response({"liked": True}, status=status.HTTP_201_CREATED)

