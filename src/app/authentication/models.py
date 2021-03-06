from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import TextChoices
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


# Create your models here.
class Role(TextChoices):
    CUSTOMER = 'customer', '顧客'
    EMPLOYEE = 'employee', '員工'
    MANAGER = 'manager', '管理者'
    SYSTEM = 'system', '系統'


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    username = None
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=10, choices=Role.choices)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
