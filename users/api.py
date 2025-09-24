from users.models import CustomUser
from rest_framework import viewsets,permissions
from users.serializers import UserSerializer
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from users.tasks import enviar_correo_verificacion
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
class UserViewSet(viewsets.ModelViewSet):
    
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
      


        try:
            user = serializer.save(is_verified=False)
        except IntegrityError:
            return Response(
            {"error": "El correo ya está registrado."},
            status=status.HTTP_400_BAD_REQUEST)
        
    
        verification_link = f"http://localhost:3000/verify/{user.verification_code}/"

   
        enviar_correo_verificacion.delay(user.name, user.email, verification_link)
        return Response(
        {"message": "Usuario creado. Revisa tu correo para verificar tu cuenta."},
        status=status.HTTP_201_CREATED
    )
class AdminLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = CustomUser.objects.get(email=email, is_admin=True)
        except CustomUser.DoesNotExist:
            return Response({"error": "Usuario admin no encontrado."}, status=404)

     
        if not check_password(password, user.password):
            return Response({"error": "Contraseña incorrecta."}, status=400)

        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Login exitoso",
            "user": {"email": user.email, "name": user.name},
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })