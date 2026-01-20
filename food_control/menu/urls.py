import django.urls

import menu.views


app_name = "menu"

urlpatterns = [
    django.urls.path(
        "",
        menu.views.MenuView.as_view(),
        name="menu",
    ),
    django.urls.path(
        "dish_detail/<int:pk>",
        menu.views.DishDetailView.as_view(),
        name="dish_detail",
    ),
    django.urls.path(
        "edit/breakfast/",
        menu.views.EditBreakfastMenuView.as_view(),
        name="edit_breakfast",
    ),
    django.urls.path(
        "edit/lunch/",
        menu.views.EditLunchMenuView.as_view(),
        name="edit_lunch",
    ),
]
