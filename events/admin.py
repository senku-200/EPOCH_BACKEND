from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Category)
admin.site.register(models.Event)
admin.site.register(models.Participant)
admin.site.register(models.Registration)
admin.site.register(models.Team)
admin.site.register(models.Incharge)