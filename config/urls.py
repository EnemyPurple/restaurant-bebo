from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("menu/", include("apps.menu.urls")),
    path("booking/", include("apps.booking.urls")),
    path("events/", include("apps.events.urls")),
    path("gallery/", include("apps.gallery.urls")),
    path("contacts/", include("apps.contacts.urls")),
    path("reviews/", include("apps.reviews.urls")),
    path("newsletter/", include("apps.newsletter.urls")),
    path("users/", include("apps.users.urls")),
    path("api/", include("apps.core.api_urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    ]

