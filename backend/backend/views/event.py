import secrets
from django.db.utils import IntegrityError
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from backend.models import Event, VerificationToken
from backend.serializers import EventSerializer
from datetime import datetime


class EventAPIView(APIView):
    def post(self, request):
        try:
            serializer = EventSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

                token = secrets.token_urlsafe(64)
                VerificationToken.objects.create(
                    token_value=token,
                    token_type='event',
                    associated_event_id=serializer.data['event_id'],
                    expiry_datetime=timezone.now() + timezone.timedelta(minutes=1)
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

    def get_by_slug(self, request, slug):
        try:
            event = Event.objects.get(event_slug=slug)
            serializer = EventSerializer(event)
            return JsonResponse(serializer.data, status=200)
        except Event.DoesNotExist:
            return JsonResponse({'error': 'Event not found'}, status=404)
        except:
            return JsonResponse({'error': 'Something went wrong'}, status=500)

    def patch(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return JsonResponse({'error': 'Event not found'}, status=404)
        except:
            return JsonResponse({'error': 'Something went wrong'}, status=500)

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

    def delete(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
            event.delete()
            return JsonResponse({}, status=204)
        except Event.DoesNotExist:
            return JsonResponse({'error': 'Event not found'}, status=404)
        except:
            return JsonResponse({'error': 'Something went wrong'}, status=500)
