from django.db.utils import IntegrityError
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Event
from .serializers import EventSerializer


@api_view(['POST'])
def create_event(request):
    if request.method == 'POST':
        try:
            serializer = EventSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse({'error': serializer.errors}, status=400)
        except IntegrityError:
            return JsonResponse({'error': 'IntegrityError'}, status=400)


@api_view(['PATCH'])
def update_event(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)

    if request.method == 'PATCH':
        try:
            serializer = EventSerializer(
                event, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=200)
            return JsonResponse(serializer.errors, status=400)
        except Exception as err:
            return JsonResponse({'error': str(err)}, status=500)
