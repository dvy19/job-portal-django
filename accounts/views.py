from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from .models import RecruiterProfile, JobSeekerProfile
from .serializers import JobSeekerProfileSerializer, LoginSerializer, RecruiterProfileSerializer, RegisterSerializer

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access":  str(refresh.access_token),
    }



class LoginView(APIView):
    permission_classes = [AllowAny]  # no auth needed to login

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            return Response(
                {
                    "message": "Login successful",
                    "role":    data["role"],
                    "tokens":  {
                        "access": data["access"],
                        "refresh": data["refresh"],
                    },
                },
                status=status.HTTP_200_OK,
            )

        # If validation fails, return the errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    permission_classes = [AllowAny]  # no auth needed to register

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user   = serializer.save()
            tokens = get_tokens_for_user(user)

            return Response(
                {
                    "message": "Registration successful",
                    "role":    user.role,
                    "tokens":  tokens,
                },
                status=status.HTTP_201_CREATED,
            )

        else:
            # This will show you exactly what failed
            #print(serializer.errors)  # Check your terminal/console
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class JobRecruiterProfileView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self, request):
        serializer=RecruiterProfileSerializer(data=request.data)

        if serializer.is_valid():
            print("User:", request.user)
            print("Is Authenticated:", request.user.is_authenticated)
            serializer.save(user=request.user)
            return Response(
                {
                    "message": "Recruiter profile created successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        
        return Response(
            {"message": "Failed to create recruiter profile", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
    
    def get(self, request):
        try:
            profile = RecruiterProfile.objects.get(user=request.user)
            serializer = RecruiterProfileSerializer(profile)

            return Response({
                "message": "Profile fetched successfully",
                "data": serializer.data
            }, status=200)

        except RecruiterProfile.DoesNotExist:
            return Response({
                "message": "Profile not found",
                "data": None
            }, status=200)




class JobSeekerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = JobSeekerProfileSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                {
                    "message": "Job seeker profile created successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        
        return Response(
            {"message": "Failed to create job seeker profile", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
    
    def get(self, request):
        try:
            profile = JobSeekerProfile.objects.get(user=request.user)
            serializer = JobSeekerProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except JobSeekerProfile.DoesNotExist:
            return Response({"message": "Job seeker profile not found"}, status=status.HTTP_404_NOT_FOUND)