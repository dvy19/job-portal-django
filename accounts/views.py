from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ForgotPasswordSerializer, ResetPasswordSerializer


from .models import CustomUser, RecruiterProfile, JobSeekerProfile, Skill
from .serializers import JobSeekerProfileSerializer, LoginSerializer, RecruiterProfileSerializer, RegisterSerializer, SkillSerializer

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access":  str(refresh.access_token),
    }

class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "If the email exists, a password reset link has been sent."},
            status=status.HTTP_200_OK
        )
    
class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Password reset successful."},
            status=status.HTTP_200_OK
        )
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

    # 🔹 CREATE PROFILE
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

    # 🔹 GET PROFILE
    def get(self, request):
        try:
            profile = JobSeekerProfile.objects.get(user=request.user)
            serializer = JobSeekerProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except JobSeekerProfile.DoesNotExist:
            return Response(
                {"message": "Job seeker profile not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    # 🔹 UPDATE PROFILE (IMPORTANT for skills)
    def put(self, request):
        try:
            profile = JobSeekerProfile.objects.get(user=request.user)
        except JobSeekerProfile.DoesNotExist:
            return Response(
                {"message": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = JobSeekerProfileSerializer(
            profile, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Profile updated successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"message": "Update failed", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
    
    def patch(self, request):
        try:
            profile = JobSeekerProfile.objects.get(user=request.user)
        except JobSeekerProfile.DoesNotExist:
            return Response(
                {"message": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = JobSeekerProfileSerializer(
            profile,
            data=request.data,
            partial=True   # always used in PATCH
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Profile updated successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"message": "Update failed", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
    


class SkillView(APIView):

    # GET all skills (for dropdown)
    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST new skill (custom skill)
    def post(self, request):
        serializer = SkillSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Skill created successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"message": "Failed to create skill", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )