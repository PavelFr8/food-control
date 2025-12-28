import django.db.models
import django.utils.safestring
from django_cleanup.signals import cleanup_pre_delete
from sorl.thumbnail import delete, get_thumbnail


def sorl_delete(**kwargs):
    delete(kwargs["file"])


cleanup_pre_delete.connect(sorl_delete)


class PublicClassImageModel(django.db.models.Model):
    image = django.db.models.ImageField(
        "Приведено к ширине 1280px",
        upload_to="core/",
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.image.name

    def get_image_x1280(self):
        return get_thumbnail(self.image, "1280", quality=51)

    def get_image_400x300(self):
        return get_thumbnail(self.image, "400x300", crop="center", quality=51)

    def get_image_300x300(self):
        return get_thumbnail(self.image, "300x300", crop="center", quality=51)

    # Для вывода в админку
    def image_tmb(self):
        return django.utils.safestring.mark_safe(
            f'<img src="{self.get_image_300x300().url}" width="50">',
        )

    image_tmb.short_description = "превью"
    image_tmb.allow_tags = True
