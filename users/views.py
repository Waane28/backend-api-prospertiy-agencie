from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import User
from .serializers import (
    UserSerializer, 
    AdminUserCreateSerializer,
    CustomerSignupSerializer,
    CustomTokenObtainPairSerializer
)
from .permissions import IsAdmin, IsSystemAdmin, IsAdminOrSystemAdmin, IsOwnerOrAdmin

# Authentication Views
class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.user
            response_data = serializer.validated_data
            
            # Optionally add user role to response
            response_data['role'] = user.role  
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': 'Invalid credentials',
                'detail': str(e)
            }, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(
                {'error': 'Invalid token', 'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

# User Management Views
class CustomerSignupView(generics.CreateAPIView):
    serializer_class = CustomerSignupSerializer
    permission_classes = [AllowAny]

class AdminCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrSystemAdmin]

    def post(self, request):
        serializer = AdminUserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Admin created successfully",
                "user_id": user.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_system_admin:
            return User.objects.all()
        elif user.is_admin:
            return User.objects.exclude(role=User.Role.SYSTEM_ADMIN)
        else:
            return User.objects.filter(id=user.id)

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin or user.is_system_admin:
            return User.objects.all()
        return User.objects.filter(id=user.id)

class PromoteToSystemAdminView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def perform_update(self, serializer):
        serializer.save(role=User.Role.SYSTEM_ADMIN)
        
