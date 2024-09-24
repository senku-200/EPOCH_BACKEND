from django.test import TestCase
from django.urls import reverse
from .models import Category, Event, Participant, Team, Registration
from rest_framework.test import APIClient
from rest_framework import status

class SymposiumTestCase(TestCase):
    
    def setUp(self):
        # Setting up the test data for Category and Events
        self.client = APIClient()
        
        # Create categories
        self.category_technical = Category.objects.create(name='Technical')
        self.category_non_technical = Category.objects.create(name='Non-Technical')
        
        # Create events
        self.event_individual = Event.objects.create(
            name="Paper Presentation",
            category=self.category_technical,
            time_limit="01:00:00",
            price=100.00,
            is_team=False
        )
        self.event_team = Event.objects.create(
            name="Coding Competition",
            category=self.category_technical,
            time_limit="02:00:00",
            price=200.00,
            is_team=True,
            max_team_size=4
        )
        
        # Create a participant
        self.participant = Participant.objects.create(
            name="John Doe",
            register_number="12345",
            email="johndoe@example.com",
            phone_number="9876543210"
        )

    def test_category_creation(self):
        category_count = Category.objects.count()
        self.assertEqual(category_count, 2)

    def test_event_creation(self):
        event_count = Event.objects.count()
        self.assertEqual(event_count, 2)
        
    def test_participant_creation(self):
        participant_count = Participant.objects.count()
        self.assertEqual(participant_count, 1)
        self.assertEqual(self.participant.email, "johndoe@example.com")

    def test_team_creation(self):
        team = Team.objects.create(event=self.event_team)
        team.members.add(self.participant)
        self.assertEqual(team.members.count(), 1)
        
    def test_individual_registration(self):
        data = {
            "participant": {
                "name": "John Doe",
                "register_number": "12345",
                "email": "johndoe@example.com",
                "phone_number": "9876543210"
            },
            "events": [
                {"event_id": self.event_individual.id}
            ]
        }
        
        response = self.client.post(reverse('register_participant'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Registration.objects.count(), 1)
    
    def test_team_registration(self):
        team_members = [
            {
                "name": "Jane Doe",
                "register_number": "67890",
                "email": "janedoe@example.com",
                "phone_number": "1234567890"
            },
            {
                "name": "Mike Smith",
                "register_number": "54321",
                "email": "mikesmith@example.com",
                "phone_number": "9871234560"
            }
        ]
        
        data = {
            "participant": {
                "name": "John Doe",
                "register_number": "12345",
                "email": "johndoe@example.com",
                "phone_number": "9876543210"
            },
            "events": [
                {
                    "event_id": self.event_team.id,
                    "team_members": team_members
                }
            ]
        }
        
        response = self.client.post(reverse('register_participant'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Team.objects.count(), 1)
        self.assertEqual(Registration.objects.count(), 1)
        team = Team.objects.first()
        self.assertEqual(team.members.count(), 3)  # John Doe + 2 team members
        
