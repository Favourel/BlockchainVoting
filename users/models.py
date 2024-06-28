from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


# Create your models here.
username_validator = RegexValidator(
    regex=r'^[@\w.+-]{1,150}$',  # Allow letters, numbers, and specific special characters
    message='Username must consist of letters, numbers, or @/./+/-/_ characters.',
    code='invalid_username'
)


class User(AbstractUser):
    username = models.CharField(_('username'), max_length=150, unique=True,
                                validators=[username_validator])
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    department = models.CharField(max_length=50, null=True, blank=True)


class Notification(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
