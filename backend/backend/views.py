from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .models import Event
from .serializers import EventSerializer


class EventAPIView(APIView):
    def post(self, request):
        try:
            serializer = EventSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse({'error': serializer.errors}, status=400)
        except IntegrityError:
            return JsonResponse({'error': 'IntegrityError'}, status=400)

    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        serializer = EventSerializer(event)
        return JsonResponse(serializer.data, status=200)

    def patch(self, request, pk):
        event = get_object_or_404(Event, pk=pk)

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

    def delete(self, request, pk):
        event = get_object_or_404(Event, pk=pk)

        try:
            event.delete()
            return JsonResponse({'message': 'Event deleted successfully'}, status=204)
        except:
            return JsonResponse({'error': 'Something went wrong'}, status=500)
