from rest_framework import serializers
from . import models

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ["name"]
class InchargeSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many = True)
    class Meta:
        model = models.Incharge
        fields = '__all__'
        
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = '__all__'
class ParticipantSerializer(serializers.ModelSerializer): 
    class Meta:
        model = models.Participant
        fields = ["name","registration_number","email","phone_number","gender"]

class TeamSerializer(serializers.ModelSerializer):
    participant = ParticipantSerializer()
    class Meta:
        model = models.Team
        fields = ["members"]

class RegistrationSerializer(serializers.ModelSerializer):
    participant = ParticipantSerializer()
    team = TeamSerializer(required = False)
    class Meta:
        model = models.Registration
        fields = ['participant','event','team','total_price','payment_status','payment_proof']