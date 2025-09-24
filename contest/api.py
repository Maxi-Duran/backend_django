
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Participant
from rest_framework.decorators import action
import random
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from contest.tasks import enviar_correo_ganador

class ParticipantViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request):
        if request.user.is_admin:  
            participants = Participant.objects.all()
        else:
            participants = Participant.objects.filter(user=request.user)

        data = [
        {
            "id": p.id,
            "user": {
                "id": p.user.id,
                "name": p.user.name,
                "email": p.user.email,
                "phone": p.user.phone,
                "is_verified": p.user.is_verified,
                "is_admin": p.user.is_admin,
                "created_at": p.user.created_at,
            },
            "participation_code": str(p.participation_code),
            "joined_at": p.joined_at,
            "is_winner": p.is_winner,
        }
        for p in participants
         ]
        return Response(data)

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
    permission_classes = [permissions.IsAuthenticated]  # Usamos is_admin en tu CustomUser

    @action(detail=False, methods=['post'])
    def select(self, request):
        user = request.user
        if not getattr(user, "is_admin", False):
            return Response({"message": "No tienes permiso"}, status=status.HTTP_403_FORBIDDEN)

        participants = list(Participant.objects.filter(is_winner=False))
        if not participants:
            return Response({"message": "No hay participantes disponibles."}, status=status.HTTP_400_BAD_REQUEST)

        winner = random.choice(participants)
        winner.is_winner = True
        winner.won_at = timezone.now()  # <-- Guardamos fecha del sorteo
        winner.save()

        enviar_correo_ganador.delay(winner.user.name, winner.user.email)

        return Response({
            "id": winner.id,
            "user": {
                "id": winner.user.id,
                "name": winner.user.name,
                "email": winner.user.email,
                "phone": winner.user.phone,
            },
            "participation_code": str(winner.participation_code),
            "won_at": winner.won_at,
            "is_winner": winner.is_winner
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def history(self, request):
        winners = Participant.objects.filter(is_winner=True).order_by("-won_at")
        data = [
            {
                "id": p.id,
                "user": {
                    "id": p.user.id,
                    "name": p.user.name,
                    "email": p.user.email,
                    "phone": p.user.phone,
                },
                "participation_code": str(p.participation_code),
                "won_at": p.won_at
            }
            for p in winners
        ]
        return Response(data)
