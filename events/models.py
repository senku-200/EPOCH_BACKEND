from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    time_limit = models.CharField(max_length=100,null=True,blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_team = models.BooleanField(default=False)
    max_team_size = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    # def clean(self):
    #     if self.is_team and (self.max_team_size is None or self.max_team_size <= 1):
    #         raise ValidationError("Team events must have a max_team_size greater than 1.")

class Participant(models.Model):
    name = models.CharField(max_length=100)
    register_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=100)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    members = models.ManyToManyField(Participant, related_name="teamMembers")

    # def clean(self):
    #     if self.members.count() > self.event.max_team_size:
    #         raise ValidationError(f"Team size cannot exceed {self.event.max_team_size} members.")

class Registration(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    payment_status = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.participant} - {self.event}"
