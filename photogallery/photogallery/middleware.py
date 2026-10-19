from django.shortcuts import redirect
from django.conf import settings

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.login_url = getattr(settings, 'LOGIN_URL', '/accounts/login/')
        
        # Pfade, die auch ohne Login erreichbar sein müssen
        self.exempt_paths = [
            self.login_url,
            '/admin/',      # Django Admin (optional, falls Admins sich dort einloggen sollen)
            '/static/',     # CSS, JS, Bilder
            '/media/',      # Hochgeladene Dateien
            # Hier kannst du weitere öffentliche URLs hinzufügen, z.B. '/registrierung/'
        ]

    def __call__(self, request):
        if not request.user.is_authenticated:
            path = request.path_info
            
            # Prüfen, ob der aktuelle Pfad eine Ausnahme ist
            is_exempt = any(path.startswith(exempt) for exempt in self.exempt_paths)
            
            if not is_exempt:
                # Umleitung zum Login mit dem ursprünglichen Pfad als Parameter (?next=...)
                return redirect(f"{self.login_url}?next={path}")

        response = self.get_response(request)
        return response