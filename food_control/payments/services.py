import django.core.exceptions
import django.db.transaction

import meals.models
import notifications.services
import payments.models


@django.db.transaction.atomic
def apply_payment(*, user, payment_type, idempotency_key):
    if payments.models.Payment.objects.filter(
        idempotency_key=idempotency_key,
        is_success=True,
    ).exists():
        return

    meals = payments.models.Payment.MEALS_MAP[payment_type]

    payments.models.Payment.objects.create(
        user=user,
        payment_type=payment_type,
        amount=150 if payment_type == "single" else 1500,
        idempotency_key=idempotency_key,
        is_success=True,
    )

    (
        access,
        _,
    ) = payments.models.FoodAccess.objects.select_for_update().get_or_create(
        user=user,
    )

    access.meals_left += meals
    access.is_active = access.meals_left > 0
    access.save(update_fields=("meals_left", "is_active"))

    notifications.services.notify_user(
        user=user,
        title="Оплата питания",
        message=(
            f"Платёж успешно выполнен. "
            f"Доступно приёмов пищи: {access.meals_left}."
        ),
        link="/users/profile/",
    )


@django.db.transaction.atomic
def consume_meal(user, meal_type):
    try:
        access = user.food_access
    except AttributeError:
        raise django.core.exceptions.PermissionDenied(
            "Доступ к питанию не активирован",
        )

    if not access.is_active or access.meals_left <= 0:
        raise django.core.exceptions.PermissionDenied(
            "Нет доступных приёмов пищи",
        )

    today = django.utils.timezone.now().date()

    try:
        meals.models.Meal.objects.create(
            user=user,
            meal_type=meal_type,
            date=today,
        )
    except django.db.IntegrityError:
        raise django.core.exceptions.PermissionDenied(
            "Приём пищи уже был отмечен сегодня",
        )

    access.meals_left -= 1

    if access.meals_left == 0:
        access.is_active = False

    access.save()
