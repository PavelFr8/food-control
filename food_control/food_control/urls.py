import django.conf
import django.conf.urls.static
import django.contrib.admin
import django.contrib.auth.urls
import django.contrib.staticfiles.urls
import django.urls

import meals.urls
import menu.urls
import menu.views
import notifications.urls
import payments.urls
import rating.urls
import users.urls
import inventory.urls


urlpatterns = [
    django.urls.path(
        "",
        menu.views.MenuView.as_view(),
        name="menu",
    ),
    django.urls.path("admin/", django.contrib.admin.site.urls),
    django.urls.path("meals/", django.urls.include(meals.urls)),
    django.urls.path("menu/", django.urls.include(menu.urls)),
    django.urls.path("users/", django.urls.include(users.urls)),
    django.urls.path("users/", django.urls.include(django.contrib.auth.urls)),
    django.urls.path("rating/", django.urls.include(rating.urls)),
    django.urls.path("payments/", django.urls.include(payments.urls)),
    django.urls.path("inventory/", django.urls.include(inventory.urls)),
    django.urls.path("notifications/", django.urls.include(notifications.urls)),
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
