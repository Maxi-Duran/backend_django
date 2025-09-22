from users.models import CustomUser
from rest_framework import viewsets,permissions
from users.serializers import UserSerializer
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(is_verified=False)  # inicialmente no verificado

    
        verification_link = f"http://localhost:8000/api/users/verify/{user.verification_code}/"

   
        send_mail(
            'Verifica tu correo',
            f'Hola {user.name}, por favor verifica tu correo haciendo clic en este enlace: {verification_link}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return Response({"message": "Usuario creado. Revisa tu correo para verificar tu cuenta."}, status=status.HTTP_201_CREATED)