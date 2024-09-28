from django.db import models
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Incharge(models.Model):
    name = models.CharField(max_length=100)
    register_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    category = models.ManyToManyField(Category, related_name='eventIncharge')
    
    def __str__(self):
        return self.name + " " + self.email

class Event(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    register_amount = models.DecimalField(max_digits=6, decimal_places=2)
    time_limit = models.CharField(max_length=100, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    is_team = models.BooleanField(default=False)
    max_team_size = models.IntegerField(null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

GENDER = [
    ('male', 'Male'),
    ('female', 'Female'),
]

class Participant(models.Model):
    name = models.CharField(max_length=100)
    register_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(choices=GENDER, max_length=10)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=100)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    members = models.ManyToManyField(Participant, related_name="teamMembers")

    def __str__(self):
        return self.name

class Registration(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    payment_status = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.participant} - {self.event}"
