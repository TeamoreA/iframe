from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.


class UserManager(BaseUserManager):
    """
    define custom user manager
    """

    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users must have a username')
        if email is None:
            raise TypeError('Users must have an email')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email)

        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        """
        create a super user
        """
        if not password:
            raise TypeError("Superuser must have a password")
        user = self.create_user(username, email, password=password)
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        """
        return username when User object is printed
        """
        return self.username

    @property
    def get_full_name(self):
        """
        return users username
        """
        return self.username
