from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Create your views here.
from rest_framework import status
from .serializers import JobSerializer
class JobView(APIView):

    permission_classes=[IsAuthenticated]

    def post(self,request):
        serializer=JobSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user.recruiterprofile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


