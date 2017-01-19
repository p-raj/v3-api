from django.conf import settings
from django.conf.urls import include, url

from asap.apps.authentication.views.login import LoginView
from asap.apps.authentication.views.token import RefreshTokenView

urlpatterns = [
    url(r'^login/$', LoginView.as_view()),
    url(r'^token/$', RefreshTokenView.as_view()),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
