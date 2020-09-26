"""Users serializers."""

# Django
from django.contrib.auth import authenticate, password_validation

# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token

# Validators
from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator

# Models
from cride.users.models import User, Profile

# Email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# JWT
import jwt

# Utilities
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer.
        THE ModelSerializer IS USED TO USE TO CREATE A TEMPLATE OF THE MODEL.
        To display the data.
    """

    class Meta:
        """Meta class."""

        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number'
        )


class UserSignUpSerializer(serializers.Serializer):
    """User sign up serializer.

    Handle sign up data validation and user/profile creation.
    """

    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    # Phone number
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: +999999999. Up to 15 digits allowed."
    )

    phone_number = serializers.CharField(
        validators=[phone_regex]
    )

    # Password
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    # Name
    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)

    def validate(self, data):
        """Verify passwords match.
            - The passwords need to be the same.
            - Validate the password with validate_password function from Django.
        """
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError("Passwords don't match.")

        # Django's Validator for passwords.
        password_validation.validate_password(passwd)
        return data

    def create(self, data):
        """Handle user and profile creation.
            - Extracts the password_confirmation.
            - Create a new user, without the password_confirmation.
            - Set up is_verified False, to add the email functionality.
            - Send_confirmation_email and return the user.
        """
        data.pop('password_confirmation')
        user = User.objects.create_user(**data, is_verified=False)
        Profile.objects.create(user=user)
        self.send_confirmation_email(user)
        return user

    def send_confirmation_email(self, user):
        """Send account verification link to given user.
            - Gets the token.
            - Set up the email.
            - We are using render to string to use a template for send a html email, and we passed the data like the context.
            - Using EmailMultiAlternatives to send the email to the user email.

        """
        verification_token = self.gen_verification_token(user)
        subject = 'Welcome @{}! Verify your account to start using Comparte Ride'.format(user.username)
        from_email = 'Comparte Ride <noreply@comparteride.com>'
        content = render_to_string(
            'emails/users/account_verification.html',
            {'token': verification_token, 'user': user}
        )
        msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
        msg.attach_alternative(content, "text/html")
        msg.send()

    def gen_verification_token(self, user):
        """Create JWT token that the user can use to verify its account.
            - Set up the expiration time.
            - Set up the payload for the token.
            - And encode the token.
        """
        exp_date = timezone.now() + timedelta(days=3)
        payload = {
            'user': user.username,
            'exp': int(exp_date.timestamp()),  # Expiration date Timestamp integer.
            'type': 'email_confirmation'
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')  # This value is in byte format.
        # To decode the payload we needs to use something like that.
        # jwt.decode(token, settings.SECRET_KEY, algorithm=['HS256'])
        return token.decode()  # This decode like a string.


class UserLoginSerializer(serializers.Serializer):
    """User login serializer.

    Handle the login request data.
    """

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Check credentials:
            - Validates that a user exist, with authenticate from.
            - raise a exception if the user is not present and if the accoun is not active yet.
            - ALL THE SERIALIZERS HAS THE ATTRIBUTE context IT USED TO USE TO SAVE DATA.
            - We was saving the user in the context to be able use it in other method.
        """
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_verified:
            raise serializers.ValidationError('Account is not active yet :(')
        self.context['user'] = user
        return data

    def create(self, data):
        """Generate or retrieve new token:
            - We are created a new token with the Token model. This needs to get a user.
            - And we return the user and the token key.
        """
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key


class AccountVerificationSerializer(serializers.Serializer):
    """Account verification serializer."""

    token = serializers.CharField()

    def validate_token(self, data):
        """Verify token is valid."""
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has expired.')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid token2')
        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Invalid token')

        self.context['payload'] = payload
        return data

    def save(self):
        """Update user's verified status.
        - Get the payload from the validate token.
        - Gets the user from the attribute user in the payload.
        - Change the is_verified field to True
        """
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_verified = True
        user.save()
