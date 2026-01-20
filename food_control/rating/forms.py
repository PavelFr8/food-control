import django.forms

from core.forms import BootstrapFormMixin
import rating.models


class RatingForm(BootstrapFormMixin, django.forms.ModelForm):
    class Meta:
        model = rating.models.Rating
        fields = (
            rating.models.Rating.mark.field.name,
            rating.models.Rating.comment.field.name,
        )
        labels = {
            rating.models.Rating.mark.field.name: "Ваша оценка",
            rating.models.Rating.comment.field.name: "Комментарии к оценке",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[rating.models.Rating.mark.field.name].choices = (
            rating.models.Rating.MarkChoice.choices
        )
