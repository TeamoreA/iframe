from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .backends import JWTAuthentication
from rest_framework import serializers, validators


User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""
    confirm_password = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        super(RegistrationSerializer, self).__init__(*args, **kwargs)

        # Override the default error_messages with a custom field error
        for field in self.fields:
            error_messages = self.fields[field].error_messages
            error_messages['null'] = error_messages['blank'] \
                = error_messages['required'] \
                = 'Please fill in the {}.'.format(field)

    email = serializers.RegexField(
        regex=r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$',
        validators=[
            validators.UniqueValidator(
                queryset=User.objects.all(),
                message='Email address already exists',
            )
        ],
    )

    # Ensure that username is unique, does not exist,
    #  cannot be left be blank, has a minimum of 5 characters
    # has alphanumerics only
    username = serializers.RegexField(
        regex=r'^[A-Za-z\-\_]+\d*$',
        min_length=4,
        max_length=30,
        required=True,
        validators=[validators.UniqueValidator(
            queryset=User.objects.all(),
            message='The username already exists. Kindly try another.'
        )],
        error_messages={
            'min_length': 'Username must have a minimum of 4 characters.',
            'max_length': 'Username must have a maximum of 30 characters.',
            'invalid': 'Username cannot only have alphanumeric characters.'
        }
    )

    # Ensure passwords are at least 8 characters long,
    # at least one letter and at least one number
    password = serializers.RegexField(
        regex=r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{7,}$",
        max_length=128,
        write_only=True,
        error_messages={
            'required': 'Password is required',
            'max_length': 'Password cannot be more than 128 characters',
            'min_length': 'Password must have at least 7 characters',
            'invalid': 'Password must have a number and a letter',
        }
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'confirm_password']

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        # remove 'confirm_password' from the validated fields
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError("Passwords do not match.")
        return attrs


class LoginSerializer(serializers.Serializer):
    """The class to serialize login details"""
    email = serializers.CharField(
        max_length=255, required=True, error_messages={
            'required': 'Email is required.'
        }
    )
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(
        max_length=128, write_only=True, required=True, error_messages={
            'required': 'Enter your password to be logged in.'
        }
    )

    def validate(self, data):
        """
        validate fields
        """
        email = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                "Your email or password is invalid"
            )
        user_data = {
            "email": user.email,
            "username": user.username
        }
        token = JWTAuthentication.generate_token(user_data)

        """
        return all required data upon successful validation
        """
        return {
            'email': user.email,
            'username': user.username,
            'token': token
        }
