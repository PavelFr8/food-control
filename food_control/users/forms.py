import django.core.exceptions
import django.forms

from core.forms import BootstrapFormMixin
from users.models import Profile, User


class SignUpForm(
    BootstrapFormMixin,
    django.contrib.auth.forms.UserCreationForm,
):
    class Meta(django.contrib.auth.forms.UserCreationForm.Meta):
        model = User
        fields = (
            User.email.field.name,
            User.username.field.name,
        )

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if "@" in username:
            raise django.core.exceptions.ValidationError(
                "Имя пользователя не может содержать символ '@'",
            )

        return username


class UserChangeForm(
    BootstrapFormMixin,
    django.contrib.auth.forms.UserChangeForm,
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("password")

    class Meta(django.contrib.auth.forms.UserChangeForm.Meta):
        model = User
        fields = (
            User.first_name.field.name,
            User.last_name.field.name,
        )


class ProfileForm(
    BootstrapFormMixin,
    django.forms.ModelForm,
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[Profile.birthday.field.name].widget = (
            django.forms.DateInput(
                attrs={"type": "date", "class": "form-control"},
            )
        )

    class Meta:
        model = Profile
        fields = (
            Profile.image.field.name,
            Profile.birthday.field.name,
        )
        help_text = {
            Profile.image.field.name: "Введите имя",
            Profile.birthday.field.name: "Введите дату дня рождения",
        }
