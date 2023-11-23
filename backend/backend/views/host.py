from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from backend.models import Host, Event
from backend.serializers import HostSerializer


class HostAPIView(APIView):
    def post(self, request):
        try:
            serializer = HostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        except:
            return JsonResponse({'error': 'Something went wrong'}, status=500)

    def get(self, request, pk):
        host = get_object_or_404(Host, pk=pk)

        try:
            serializer = HostSerializer(host)
            return JsonResponse(serializer.data, status=200)
        except Host.DoesNotExist:
            return JsonResponse({'error': 'Host not found'}, status=404)
        except:
            return JsonResponse({'error': 'Something went wrong'}, status=500)

    def patch(self, request, pk):
        self.permission_classes = [IsAuthenticated]

        authorization_token = request.headers.get('Authorization')
        if not authorization_token:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        host = get_object_or_404(Host, pk=pk)

        if authorization_token != host.event.edit_token:
            return JsonResponse({'error': 'Authorization token mismatch'}, status=401)

        try:
            serializer = HostSerializer(host, data=request.data, partial=True)
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

        host = get_object_or_404(Host, pk=pk)

        if authorization_token != host.event.edit_token:
            return JsonResponse({'error': 'Authorization token mismatch'}, status=401)

        try:
            host.delete()
            return JsonResponse({}, status=204)
        except:
            return JsonResponse({'error': 'Something went wrong'}, status=500)
