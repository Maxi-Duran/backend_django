# contest/serializers.py
from rest_framework import serializers
from .models import Participant

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['id', 'user', 'joined_at', 'participation_code', 'is_winner']
        read_only_fields = ['id', 'joined_at', 'participation_code', 'is_winner']
