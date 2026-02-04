import django.urls

import meals.views


app_name = "meals"

urlpatterns = [
    django.urls.path(
        "",
        meals.views.MealsView.as_view(),
        name="meals",
    ),
    django.urls.path(
        "consume/<int:user_id>/<str:meal_type>/",
        meals.views.ConsumeMealView.as_view(),
        name="consume_meal",
    ),
]
