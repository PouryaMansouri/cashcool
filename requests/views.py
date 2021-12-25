from django.http import JsonResponse
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from .permissions import IsMarketer
from .serializers import ImportUserRequestSerializer
from .tasks import import_user_request_excel_file_process


class ImportUserRequestView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsMarketer]
    serializer_class = ImportUserRequestSerializer


def celery(request):
    import_user_request_excel_file_process.delay()
    return JsonResponse('done', safe=False)
    
    
    
    #demo
