from rest_framework import status, mixins
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import CustomUser, Role
from .serializers import AuthTokenSerializer, UserSerializer, EmployeeSerializer, CustomerSerializer


# Create your views here.
class AuthViewSet(GenericViewSet):
    serializer_class = AuthTokenSerializer
    permission_classes = (AllowAny,)

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    @action(detail=False)
    def me(self, request):
        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CustomerViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    queryset = CustomUser.objects.filter(role=Role.CUSTOMER)
    serializer_class = CustomerSerializer


class EmployeeViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    queryset = CustomUser.objects.filter(role__in=[Role.EMPLOYEE, Role.MANAGER])
    serializer_class = EmployeeSerializer

    def get_serializer(self, *args, **kwargs):
        if self.action == 'import_employees':
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)

    @action(detail=False, methods=['post'], url_path='import')
    def import_employees(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
