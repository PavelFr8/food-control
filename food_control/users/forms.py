import django.contrib.auth.mixins
import django.core.exceptions
import django.forms

from core.forms import BootstrapFormMixin
import users.models


class RoleRequiredMixin(django.contrib.auth.mixins.LoginRequiredMixin):
    required_roles = [users.models.Role.RoleNames.STUDENT]

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        allow_access = False
        for role in self.required_roles:
            if role is None or role not in users.models.Role.RoleNames:
                raise RuntimeError(
                    f"{self.__class__.__name__} requires `required_role`",
                )

            if request.user.role.name == role:
                allow_access = True
                break

        if not allow_access:
            raise django.core.exceptions.PermissionDenied

        return super().dispatch(request, *args, **kwargs)


class SignUpForm(
    BootstrapFormMixin,
    django.contrib.auth.forms.UserCreationForm,
):
    class Meta(django.contrib.auth.forms.UserCreationForm.Meta):
        model = users.models.User
        fields = (
            users.models.User.email.field.name,
            users.models.User.last_name.field.name,
            users.models.User.first_name.field.name,
            users.models.User.patronymic.field.name,
            users.models.User.birthday.field.name,
            users.models.User.school_class.field.name,
        )
        widgets = {
            users.models.User.birthday.field.name: django.forms.DateInput(
                attrs={"type": "date"},
            ),
        }


class UserForm(
    BootstrapFormMixin,
    django.forms.ModelForm,
):
    class Meta:
        model = users.models.User
        fields = (
            users.models.User.email.field.name,
            users.models.User.last_name.field.name,
            users.models.User.first_name.field.name,
            users.models.User.patronymic.field.name,
            users.models.User.birthday.field.name,
            users.models.User.school_class.field.name,
            users.models.User.food_features.field.name,
        )
        widgets = {
            users.models.User.birthday.field.name: django.forms.DateInput(
                attrs={"type": "date"},
            ),
        }
        help_texts = {
            users.models.User.birthday.field.name: "Введите дату рождения",
        }


class UserFoodFeaturesForm(django.forms.ModelForm):
    class Meta:
        model = users.models.User
        fields = ("food_features",)
        widgets = {
            "food_features": django.forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["food_features"].queryset = (
            users.models.FoodFeatures.objects.order_by("name")
        )
