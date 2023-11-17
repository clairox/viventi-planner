import secrets
from django.http import JsonResponse
from django.utils import timezone
from rest_framework.decorators import api_view
from backend.models import VerificationToken, Event, EventRsvp


@api_view(['POST'])
def verify_event(request, token):
    try:
        token = VerificationToken.objects.get(token_value=token)
        if token.expiry_datetime >= timezone.now():
            event_slug = secrets.token_urlsafe(16)
            edit_token = secrets.token_hex(32)

            event = Event.objects.get(event_id=token.associated_event_id)
            if event.verified:
                return JsonResponse({'message': 'Event already verified'}, status=200)

            event.status = 'verified'
            event.verified = True
            event.event_slug = event_slug
            event.edit_token = edit_token
            event.save()

            return JsonResponse({'message': 'Event verified successfully'}, status=200)
        else:
            return JsonResponse({'message': 'Verification token expired'}, status=200)
    except VerificationToken.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)
    except:
        return JsonResponse({'error': 'Something went wrong'}, status=500)


@api_view(['POST'])
def verify_rsvp(request, token):
    try:
        token = VerificationToken.objects.get(token_value=token)
        if token.expiry_datetime >= timezone.now():
            edit_token = secrets.token_hex(32)

            rsvp = EventRsvp.objects.get(rsvp_id=token.associated_rsvp_id)
            if rsvp.verified:
                return JsonResponse({'message': 'Event RSVP already verified'}, status=200)

            rsvp.verified = True
            rsvp.edit_token = edit_token
            rsvp.save()

            return JsonResponse({'message': 'Event RSVP verified successfully'}, status=200)
        else:
            return JsonResponse({'message': 'Verification token expired'}, status=200)
    except VerificationToken.DoesNotExist:
        return JsonResponse({'error': 'Event RSVP not found'}, status=404)
    except:
        return JsonResponse({'error': 'Something went wrong'}, status=500)
