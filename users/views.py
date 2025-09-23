from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .models import CustomUser
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView
# Create your views here.
class VerifyUserView(APIView):
    def get(self, request, code):
        try:
            user = CustomUser.objects.get(verification_code=code)
            user.is_verified = True
            user.save()
            return Response({"message": "Correo verificado. Ahora puedes establecer tu contraseña."})
        except CustomUser.DoesNotExist:
            return Response({"error": "Código de verificación inválido."}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, code):
        try:
            user = CustomUser.objects.get(verification_code=code)
            password = request.data.get('password')
            if not password:
                return Response({"error": "Se requiere una contraseña."}, status=status.HTTP_400_BAD_REQUEST)
            user.password = password 
            user.save()
            return Response({"message": "Contraseña creada. Tu cuenta está activa."})
        except CustomUser.DoesNotExist:
            return Response({"error": "Código de verificación inválido."}, status=status.HTTP_400_BAD_REQUEST)
