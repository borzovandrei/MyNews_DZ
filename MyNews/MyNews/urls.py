from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('News.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
