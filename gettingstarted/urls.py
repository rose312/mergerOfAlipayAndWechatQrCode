from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

from django.conf.urls.static import static
from django.conf import settings

import hello.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^', include('hello.urls', namespace='hello')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
