from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from .models import CustomUser, Role, Employee


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)

            # The authenticate call simply returns None for is_active=False users.
            # (Assuming the default ModelBackend authentication backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        instance = super().save(**kwargs)

        validated_data = {**self.validated_data, **kwargs}
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
            instance.save()

        return instance

    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }


class EmployeeListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        users = []
        for data in validated_data:
            user = CustomUser(**data)
            if user.password:
                user.set_password(user.password)
            users.append(user)
        users = CustomUser.objects.bulk_create(users)

        employees = [Employee(user=user) for user in users]
        Employee.objects.bulk_create(employees)
        return users


class EmployeeSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        attrs['role'] = Role.EMPLOYEE
        return super().validate(attrs)

    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'read_only': True}
        }
        list_serializer_class = EmployeeListSerializer
