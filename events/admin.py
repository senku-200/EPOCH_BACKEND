from django.contrib import admin
from django.core.mail import send_mail
from .models import Registration, Event, Participant, Team, Category, Incharge
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from decouple import config

email_sender = config("EMAIL_HOST_USER")

class RegistrationInline(admin.TabularInline):
    model = Registration
    extra = 0

class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']
    search_fields = ['name', 'email']
    list_filter = ['registration__event', 'registration__payment_status']
    inlines = [RegistrationInline]

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['participant', 'event', 'total_amount', 'payment_status', 'registered_at']
    search_fields = ['participant__name', 'event__name']
    list_filter = ['event', 'payment_status', 'event__day','participant__college']

    def save_model(self, request, obj, form, change):
        if obj.payment_status:
            Registration.objects.filter(participant=obj.participant).update(payment_status=True)

            events = Registration.objects.filter(participant=obj.participant)
            event_list = [reg.event for reg in events] 

            context = {
                'participant': obj.participant,
                'events': event_list,
            }

            html_message = render_to_string('emails/registration_confirmation.html', context)
            plain_message = strip_tags(html_message)
            from_email = email_sender
            recipient_list = [obj.participant.email]

            send_mail(
                'Registration Payment Confirmed',
                plain_message, 
                from_email,
                recipient_list,
                html_message=html_message,  
                fail_silently=False,
            )

        super().save_model(request, obj, form, change)

admin.site.register(Participant)
admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Event)
admin.site.register(Team)
admin.site.register(Category)
admin.site.register(Incharge)

