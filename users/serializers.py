from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .permissions import IsOwnerOrAdmin  # Add this import at the top


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=False  # Make email optional for updates
    )
    phone_number = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=False  # Make phone_number optional for updates
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                'phone_number', 'role', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'read_only': True},
            'is_active': {'read_only': True},
            'username': {'read_only': True}  # Typically usernames shouldn't change
        }

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Enter a valid email address.")
        return value

    def validate_phone_number(self, value):
        if value and not value.startswith('+'):
            raise serializers.ValidationError("Phone number must start with country code (e.g., +1)")
        return value

    def validate(self, attrs):
        # Get the request user from context
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            
            # For non-admin users, prevent changing certain fields
            if not (user.is_admin or user.is_system_admin):
                # Remove fields that customers shouldn't be able to modify
                restricted_fields = ['role', 'is_active']
                for field in restricted_fields:
                    attrs.pop(field, None)
                
                # Ensure customers can only update their own profile
                if self.instance and self.instance != user:
                    raise serializers.ValidationError(
                        "You can only update your own profile."
                    )
        
        return attrs

    def update(self, instance, validated_data):
        # Handle password separately if it's included
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        
        return super().update(instance, validated_data)

class AdminUserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 
                'last_name', 'phone_number', 'role']
        extra_kwargs = {
            'phone_number': {'required': True},
            'role': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class CustomerSignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 
                'last_name', 'phone_number']
        extra_kwargs = {
            'phone_number': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        validated_data['role'] = User.Role.CUSTOMER
        user = User.objects.create_user(**validated_data)
        return user

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True,
        validators=[validate_password]
    )
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs
    
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['email'] = user.email
        token['role'] = user.role
        token ['userId'] = user.id 

        return token

    # def validate(self, attrs):
    #     data = super().validate(attrs)
    #     # Add extra responses here
    #     data.update({
    #         'user': {
    #             'id': self.user.id,
    #             'email': self.user.email,
    #             'role': self.user.role,
    #             'first_name': self.user.first_name,
    #             'last_name': self.user.last_name
    #         }
    #     })
    #     return data