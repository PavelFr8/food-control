import django.conf
import django.conf.urls.static
import django.contrib.admin
import django.contrib.auth.urls
import django.contrib.staticfiles.urls
import django.urls

import homepage.urls
import users.urls


urlpatterns = [
    django.urls.path("", django.urls.include(homepage.urls)),
    django.urls.path("admin/", django.contrib.admin.site.urls),
    django.urls.path("users/", django.urls.include(users.urls)),
    django.urls.path("users/", django.urls.include(django.contrib.auth.urls)),
]


if django.conf.settings.DEBUG:
    if django.conf.settings.MEDIA_ROOT:
        urlpatterns += django.conf.urls.static.static(
            django.conf.settings.MEDIA_URL,
            document_root=django.conf.settings.MEDIA_ROOT,
        )

    urlpatterns += django.contrib.staticfiles.urls.staticfiles_urlpatterns()

    import debug_toolbar.urls

    urlpatterns += (
        django.urls.path(
            "__debug__/",
            django.urls.include(debug_toolbar.urls),
        ),
    )
