from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import TextChoices
from django.utils.translation import ugettext_lazy as _

from utils.models import BaseModel
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

    @property
    def is_customer(self):
        return self.role == Role.CUSTOMER and hasattr(self, 'customer')

    @property
    def is_employee(self):
        return self.role in [Role.EMPLOYEE, Role.MANAGER] and hasattr(self, 'employee')

    def __str__(self):
        return self.email


class Customer(BaseModel):
    id = models.UUIDField(default=uuid4, editable=False)
    user = models.OneToOneField('CustomUser', primary_key=True, on_delete=models.CASCADE, verbose_name='使用者')
    nick_name = models.CharField(max_length=10, null=True, blank=True)

    def clean(self):
        if self.user.is_employee:
            raise ValidationError(_('This user is already set as an employee.'))


class Employee(BaseModel):
    id = models.UUIDField(default=uuid4, editable=False)
    user = models.OneToOneField('CustomUser', primary_key=True, on_delete=models.CASCADE, verbose_name='使用者')
    nick_name = models.CharField(max_length=10, null=True, blank=True)

    def clean(self):
        if self.user.is_customer:
            raise ValidationError(_('This user is already set as a customer.'))
