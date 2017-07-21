"""
Veris URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from rest_framework.documentation import include_docs_urls
from rest_framework_nested import routers
from rest_framework_swagger.views import get_swagger_view

from asap.apps.process.views import ProcessViewSet
from asap.apps.runtime.views import FeedbackViewSet, SessionViewSet
from asap.apps.runtime.views.runtime import RuntimeViewSet
from asap.apps.runtime.views.widget_process_execution import WidgetProcessExecution
from asap.apps.widget.views import WidgetViewSet
from asap.utils.views.revision import RevisionViewSet
from asap.utils.views.version import VersionViewSet

from .router import Router

r = Router()
r.register('processes', ProcessViewSet)
r.register('widgets', WidgetViewSet)

r.register('runtimes', RuntimeViewSet)
r.register('feedbacks', FeedbackViewSet)
r.register('sessions', SessionViewSet, base_name='runtimesession')

r.register('version', VersionViewSet)
r.register('revision', RevisionViewSet)

r_widget = routers.NestedSimpleRouter(r, 'widgets', lookup='widget')
r_widget.register('processes', ProcessViewSet)

r_runtime = routers.NestedSimpleRouter(r, 'runtimes', lookup='app')
r_runtime.register('feedbacks', FeedbackViewSet)
r_runtime.register('sessions', SessionViewSet, base_name='runtime-session')
r_runtime.register('widgets', WidgetViewSet, base_name='runtime-widget')

API_TITLE = 'NoApp API'

urlpatterns = [
    url(r'^schema/$', get_swagger_view(title=API_TITLE)),
    url(r'^docs/', include_docs_urls(title=API_TITLE, description='')),

    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^api/v1/', include(r.urls)),
    url(r'^api/v1/', include(r_widget.urls)),
    url(r'^api/v1/', include(r_runtime.urls)),

    url(r'^api/v1/widgets/(?P<widget_uuid>.*(?=/))/(?P<action>.*(?=/))/$',
        WidgetProcessExecution.as_view(), name='widget-action'),
    url(r'^api/v1/runtimes/(?P<uuid>.*(?=/))/widgets/(?P<widget_uuid>.*(?=/))/(?P<action>.*(?=/))/$',
        WidgetProcessExecution.as_view(), name='runtime-widget-action'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
