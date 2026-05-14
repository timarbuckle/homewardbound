from django.conf import settings

def version_renderer(request):
    return {'GCP_VERSION': settings.GCP_VERSION}
