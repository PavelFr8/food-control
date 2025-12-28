from django.contrib.auth import views
import django.urls

import users.views

app_name = "users"

urlpatterns = []

# Signing up and logging in
urlpatterns += [
    django.urls.path(
        "login/",
        views.LoginView.as_view(
            template_name="users/login.html",
        ),
        name="login",
    ),
    django.urls.path(
        "logout/",
        views.LogoutView.as_view(
            template_name="users/logout.html",
        ),
        name="logout",
    ),
    django.urls.path(
        "signup/",
        users.views.SignUpView.as_view(),
        name="signup",
    ),
    django.urls.path(
        "activate/<str:username>",
        users.views.ActivateView.as_view(),
        name="activate",
    ),
    django.urls.path(
        "reactivate/<int:pk>",
        users.views.ReactivateView.as_view(),
        name="reactivate",
    ),
]

# Password change and reset
urlpatterns += [
    django.urls.path(
        "password_change/",
        views.PasswordChangeView.as_view(
            template_name="users/password_change.html",
        ),
        name="password_change",
    ),
    django.urls.path(
        "password_change/done/",
        views.PasswordChangeDoneView.as_view(
            template_name="users/password_change_done.html",
        ),
        name="password_change_done",
    ),
    django.urls.path(
        "password_reset/",
        users.views.CustomPasswordResetView.as_view(),
        name="password_reset",
    ),
    django.urls.path(
        "password_reset/done/",
        views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    django.urls.path(
        "password_reset/confirm/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            success_url=django.urls.reverse_lazy(
                "users:password_reset_complete",
            ),
        ),
        name="password_reset_confirm",
    ),
    django.urls.path(
        "password_reset/complete/",
        views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
]

# User profile and list
urlpatterns += [
    django.urls.path(
        "user_list/",
        users.views.UserListView.as_view(),
        name="user_list",
    ),
    django.urls.path(
        "user_details/<int:pk>",
        users.views.UserDetailView.as_view(),
        name="user_detail",
    ),
    django.urls.path(
        "profile/",
        users.views.ProfileView.as_view(),
        name="profile",
    ),
]
