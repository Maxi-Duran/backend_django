from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import CustomUser
from contest.models import Participant
from django.contrib.auth.hashers import make_password
from rest_framework import permissions
class VerifyUserView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, code):
        try:
            user = CustomUser.objects.get(verification_code=code)
            user.is_verified = True
            user.save()
            if not Participant.objects.filter(user=user).exists():
                    Participant.objects.create(user=user)
            return Response({"message": "Correo verificado. Ahora puedes establecer tu contraseña."})
        except CustomUser.DoesNotExist:
            return Response({"error": "Código de verificación inválido."}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, code):
        try:
            user = CustomUser.objects.get(verification_code=code)
            password = request.data.get('password')
            if not password:
                return Response({"error": "Se requiere una contraseña."}, status=status.HTTP_400_BAD_REQUEST)
            
 
            user.password = make_password(password)
            user.save()
            
            return Response({"message": "Contraseña creada. Tu cuenta está activa."})
        except CustomUser.DoesNotExist:
            return Response({"error": "Código de verificación inválido."}, status=status.HTTP_400_BAD_REQUEST)
