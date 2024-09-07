import django
from pathlib import Path

from django.conf import settings
from django.contrib.staticfiles import finders
from django.http import FileResponse, HttpRequest, HttpResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET

if django.VERSION[:2] >= (5, 1):
    from django.contrib.auth.decorators import login_not_required
else:

    def login_not_required(view_func):
        return view_func


CACHE_TIME_FAVICON = getattr(settings, "CACHE_TIME_FAVICON", 60 * 60 * 24)  # 1 day


@require_GET
@cache_control(
    max_age=0 if settings.DEBUG else CACHE_TIME_FAVICON, immutable=True, public=True
)
@login_not_required
def favicon(request: HttpRequest) -> HttpResponse | FileResponse:
    name = request.path.lstrip("/")
    if path := finders.find(name):
        return FileResponse(Path(path).read_bytes())
    return HttpResponse(
        (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
            '<text y=".9em" font-size="90">🚀</text>'
            "</svg>"
        ),
        content_type="image/svg+xml",
    )
