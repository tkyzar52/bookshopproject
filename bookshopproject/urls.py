from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bookshop/',include('bookshop_app.urls')),
    path('', include('accounts.urls')),
     

]

urlpatterns += static(
    # MEDIA_URL = 'media/'
    settings.MEDIA_URL,
    # MEDIA_ROOTにリダイレクト
    document_root=settings.MEDIA_ROOT
)
