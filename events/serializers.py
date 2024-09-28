from rest_framework import serializers
from .models import Category, Incharge, Event, Participant, Team, Registration

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]

class InchargeSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)

    class Meta:
        model = Incharge
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    members = ParticipantSerializer(many=True)  # Update to handle many-to-many

    class Meta:
        model = Team
        fields = '__all__'

class RegistrationSerializer(serializers.ModelSerializer):
    participant = ParticipantSerializer()
    team = TeamSerializer(required=False)

    class Meta:
        model = Registration
        fields = '__all__'
