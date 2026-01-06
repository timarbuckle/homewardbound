from django.utils.cache import patch_cache_control

class MediaCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Only apply to successful media requests
        if request.path.startswith('/media/') and response.status_code == 200:
            # public: allowed to be cached by CDNs (Cloudflare)
            # max-age: browser cache (in seconds)
            # s-maxage: Cloudflare specific cache (30 days)
            patch_cache_control(response, public=True, max_age=2592000, s_maxage=2592000)
            
        return response
