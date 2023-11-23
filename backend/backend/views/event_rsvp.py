import secrets
from django.db.utils import IntegrityError
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from backend.models import EventRsvp, VerificationToken, Event
from backend.serializers import EventRsvpSerializer, EventRsvpWithAttendeeAuthSerializer, EventRsvpWithOrganizerAuthSerializer


class EventRsvpAPIView(APIView):

    def post(self, request):
        request.data['blocked'] = False
        print(request.data)
        try:
            serializer = EventRsvpSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

                token = secrets.token_urlsafe(64)
                VerificationToken.objects.create(
                    token_value=token,
                    token_type='rsvp',
                    associated_rsvp_id=serializer.data['rsvp_id'],
                    expiry_datetime=timezone.now() + timezone.timedelta(days=1)
                )
                return JsonResponse(serializer.data, status=201)
            return JsonResponse({'error': serializer.errors}, status=400)
        except IntegrityError:
            return JsonResponse({'error': 'IntegrityError'}, status=400)
        except:
            return JsonResponse({'error': 'Something went wrong'}, status=500)

    def get(self, request, pk):
        rsvp = get_object_or_404(EventRsvp, pk=pk)

        try:
            serializer = EventRsvpSerializer(rsvp)
            return JsonResponse(serializer.data, status=200)
        except EventRsvp.DoesNotExist:
            return JsonResponse({'error': 'Event RSVP not found'}, status=404)
        except:
            return JsonResponse({'error': 'Something went wrong'}, status=500)

    def patch(self, request, pk):
        self.permission_classes = [IsAuthenticated]

        authorization_token = request.headers.get('Authorization')
        if not authorization_token:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        rsvp = get_object_or_404(EventRsvp, pk=pk)
        event = get_object_or_404(Event, pk=rsvp.event_id)

        if authorization_token != rsvp.edit_token and authorization_token != event.edit_token:
            return JsonResponse({'error': 'Authorization token mismatch'}, status=401)

        try:
            if authorization_token == rsvp.edit_token:
                serializer = EventRsvpWithAttendeeAuthSerializer(
                    rsvp, data=request.data, partial=True
                )
            else:
                serializer = EventRsvpWithOrganizerAuthSerializer(
                    rsvp, data=request.data, partial=True
                )
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=200)
            return JsonResponse(serializer.errors, status=400)
        except:
            return JsonResponse({'error': 'Something went wrong'}, status=500)

    def delete(self, request, pk):
        self.permission_classes = [IsAuthenticated]

        authorization_token = request.headers.get('Authorization')
        if not authorization_token:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        rsvp = get_object_or_404(EventRsvp, pk=pk)

        if authorization_token != rsvp.edit_token:
            return JsonResponse({'error': 'Authorization token mismatch'}, status=401)
        try:
            rsvp.delete()
            return JsonResponse({}, status=204)
        except:
            return JsonResponse({'error': 'Something went wrong'}, status=500)
