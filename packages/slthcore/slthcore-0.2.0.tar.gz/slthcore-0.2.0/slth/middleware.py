from django.middleware.security import SecurityMiddleware
class SecurityHeadersMiddleware:
    """
        * Strict-Transport-Security: Enforces the use of HTTPS.
        * X-Content-Type-Options: Prevents the browser from interpreting files as a different MIME type.
        * Content-Security-Policy: Helps prevent cross-site scripting (XSS) and other code injection attacks.
        * Referrer-Policy: Controls the amount of referrer information included with requests.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response['X-Content-Type-Options'] = 'nosniff'
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; "
            "connect-src 'self';"
        )
        response['Referrer-Policy'] = 'no-referrer'
        return response
