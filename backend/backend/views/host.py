from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from backend.models import Host
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
        host = get_object_or_404(Host, pk=pk)

        try:
            serializer = HostSerializer(host, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=200)
            return JsonResponse(serializer.errors, status=400)
        except:
            return JsonResponse({'error': 'Something went wrong'}, status=500)

    def delete(self, request, pk):
        host = get_object_or_404(Host, pk=pk)

        try:
            host.delete()
            return JsonResponse({}, status=204)
        except Host.DoesNotExist:
            return JsonResponse({'error': 'Host not found'}, status=404)
        except:
            return JsonResponse({'error': 'Something went wrong'}, status=500)
