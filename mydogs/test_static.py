from django.http import HttpResponse
from django.conf import settings
import os

def serve_static(request, path):
    file_path = os.path.join(settings.STATIC_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            return HttpResponse(file.read(), content_type="text/css")
    else:
        return HttpResponse("File not found", status=404)