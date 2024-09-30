from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status,viewsets
from django.db import transaction
from .models import Event, Participant, Registration, Team,Incharge,Category
from .serializers import RegistrationSerializer,EventSerializer,InchargeSerializer,CategorySerializer
from django.core.exceptions import ObjectDoesNotExist

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
class InchargeViewSet(viewsets.ModelViewSet):
    queryset = Incharge.objects.all()
    serializer_class = InchargeSerializer
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
class registerViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer

def get_or_create_participant(participant_data):
    participant, created = Participant.objects.get_or_create(
        email=participant_data['email'],
        defaults={
            'register_number': participant_data['register_number'],
            'name': participant_data['name'],
            'phone_number': participant_data['phone_number']
        }
    )
    return participant

def handle_team_registration(participant, team_data, event):
    team_name = f"Team {participant.name} - {event.name}"
    team, created = Team.objects.get_or_create(event=event, name=team_name)
    team.members.add(participant)
    for member_data in team_data:
        member = get_or_create_participant(member_data)
        team.members.add(member)
    
    return team


def register_to_event(participant, event, team=None,total_amount=0):
    registration = Registration.objects.create(
        participant=participant,
        event=event,
        team=team,
        total_amount=total_amount,
        payment_status=False
    )
    return registration

def handle_registration(participant, event, team_members_details=None,total_amount = 0):
    if event.is_team and team_members_details:
        team = handle_team_registration(participant, team_members_details, event)
        return register_to_event(participant, event, team,total_amount=total_amount)
    else:
        return register_to_event(participant, event,total_amount=total_amount)


@api_view(['POST'])
@transaction.atomic
def register_participant(request):
    try:
        data = request.data
        participant_data = data.get('participant')
        events_data = data.get('events', [])
        total_amount = data.get('total_amount')
        

        if not participant_data or not events_data:
            return Response({'error': 'Participant and events data are required'}, status=status.HTTP_400_BAD_REQUEST)

        participant = get_or_create_participant(participant_data)
        registered_events = []

        for event_data in events_data:
            event_id = event_data.get('id')
            team_members_details = event_data.get('team_members', None)
            try:
                event = Event.objects.get(id=event_id)
            except ObjectDoesNotExist:
                return Response({'error': f'Event with ID {event_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)

            registration = handle_registration(participant, event, team_members_details,total_amount=total_amount)
            registered_events.append(registration)

        return Response({'status': 'Registration successful!'}, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
