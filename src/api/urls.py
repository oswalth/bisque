from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from api.flats.views import FlatViewSet, BuildingViewSet, ResidentialViewSet, AddressViewSet

api_router = routers.DefaultRouter()

router = routers.DefaultRouter()
router.register(r"addresses", AddressViewSet)
router.register(r"residentials", ResidentialViewSet)
router.register(r"buildings", BuildingViewSet)
router.register(r"flats", FlatViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include((router.urls, 'flats'))),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    if settings.ENABLE_DEBUG_TOOLBAR:
        import debug_toolbar

        urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
