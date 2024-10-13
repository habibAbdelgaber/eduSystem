from django.conf import settings
from django.contrib import admin
from django.urls import path, include
# from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf.urls.static import static
from django.views.generic import TemplateView

from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls', namespace='core')),
    path('',
         TemplateView.as_view(template_name='core/index.html'),
         name='index'),
    path('common-err-page/',
         views.common_err_handler_view,
         name='common-err-page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
