
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Participant

import random
from django.core.mail import send_mail
from django.conf import settings

class ParticipantViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        user = request.user
        if not user.is_verified:
            return Response({"message": "Debes verificar tu correo antes de participar."}, status=status.HTTP_403_FORBIDDEN)

      
        if Participant.objects.filter(user=user).exists():
            return Response({"message": "Ya estás participando."}, status=status.HTTP_400_BAD_REQUEST)

        participant = Participant.objects.create(user=user)

   
        send_mail(
            subject="Confirmación de participación",
            message=f"Hola {user.name}, tu participación ha sido registrada correctamente. Código: {participant.participation_code}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return Response({"message": "Participación confirmada. Revisa tu correo."}, status=status.HTTP_201_CREATED)


class WinnerSelectionViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        participants = list(Participant.objects.filter(is_winner=False))
        if not participants:
            return Response({"message": "No hay participantes disponibles."}, status=status.HTTP_400_BAD_REQUEST)

        winner = random.choice(participants)
        winner.is_winner = True
        winner.save()

  
        send_mail(
            subject="¡Felicidades! Has ganado",
            message=f"Hola {winner.user.name}, ¡felicidades! Has sido seleccionado como ganador del concurso.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[winner.user.email],
            fail_silently=False,
        )

        return Response({"message": f"Ganador seleccionado: {winner.user.email}"}, status=status.HTTP_200_OK)
