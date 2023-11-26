import secrets
from django.db.utils import IntegrityError
from django.utils import timezone
from django.utils.html import strip_tags
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from backend.models import Event, VerificationToken
from backend.serializers import EventSerializer
from backend.config import useConfig

config = useConfig('local')


def send_verification_email(token, recipient):
    subject = 'Verify your email'
    message = render_to_string('email/verification_email.html', {
        'url': f'{config('CLIENT_URL')}/event/activate/{token}/'
    })
    plain_message = strip_tags(message)
    from_email = config('FROM_EMAIL')

    send_mail(
        subject,
        plain_message,
        from_email,
        [recipient],
        html_message=message)


class EventAPIView(APIView):
    def post(self, request):
        try:
            serializer = EventSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

                token = secrets.token_urlsafe(64)
                verification_token = VerificationToken.objects.create(
                    token_value=token,
                    token_type='event',
                    associated_event_id=serializer.data['event_id'],
                    expiry_datetime=timezone.now() + timezone.timedelta(hours=24)
                )

                send_verification_email(
                    verification_token.token_value,
                    serializer.data['organizer_email']
                )

                return JsonResponse(serializer.data, status=201)
            return JsonResponse({'error': serializer.errors}, status=400)
        except IntegrityError:
            return JsonResponse({'error': 'IntegrityError'}, status=400)
        except:
            return JsonResponse({'error': 'Something went wrong'}, status=500)

    def get(self, request, identifier):
        if identifier.isdigit():
            event = get_object_or_404(Event, pk=identifier)
        else:
            event = get_object_or_404(Event, event_slug=identifier)

        try:
            serializer = EventSerializer(event)
            return JsonResponse(serializer.data, status=200)
        except Event.DoesNotExist:
            return JsonResponse({'error': 'Event not found'}, status=404)
        except:
            return JsonResponse({'error': 'Something went wrong'}, status=500)

    def patch(self, request, identifier):
        self.permission_classes = [IsAuthenticated]

        authorization_token = request.headers.get('Authorization')
        if not authorization_token:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        try:
            if identifier.isdigit():
                event = get_object_or_404(Event, pk=identifier)
            else:
                event = get_object_or_404(Event, event_slug=identifier)
        except Event.DoesNotExist:
            return JsonResponse({'error': 'Event not found'}, status=404)
        except:
            return JsonResponse({'error': 'Something went wrong'}, status=500)

        if authorization_token != event.edit_token:
            return JsonResponse({'error': 'Authorization token mismatch'}, status=401)

        try:
            serializer = EventSerializer(
                event, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=200)
            return JsonResponse(serializer.errors, status=400)
        except:
            return JsonResponse({'error': 'Something went wrong'}, status=500)

    def delete(self, request, identifier):
        self.permission_classes = [IsAuthenticated]

        authorization_token = request.headers.get('Authorization')
        if not authorization_token:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        try:
            if identifier.isdigit():
                event = get_object_or_404(Event, pk=identifier)
            else:
                event = get_object_or_404(Event, event_slug=identifier)

            if authorization_token != event.edit_token:
                return JsonResponse({'error': 'Authorization token mismatch'}, status=401)

            event.delete()
            return JsonResponse({}, status=204)
        except Event.DoesNotExist:
            return JsonResponse({'error': 'Event not found'}, status=404)
        except:
            return JsonResponse({'error': 'Something went wrong'}, status=500)
