
# for importing images (not recommended during production)
from  django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

# # rather the importing include we can add urls like this
# from app.views import home, contact


urlpatterns = [
    path('items/', include('item.urls')),
    path('', include('app.urls')),
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('message/', include('messaging.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # to be able to post images
