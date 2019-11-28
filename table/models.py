from django.db import models
from django.conf import settings
from django.utils.text import slugify

from main.utils import NonDeletedManager
from slug.utils import unique_slug


class Table(models.Model):

    obs = NonDeletedManager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, allow_unicode=True, null=True)

    is_deleted = models.BooleanField(default=False, db_index=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        slug = slugify(self.name)
        self.slug = unique_slug('Table', slug)

        return super().save(*args, **kwargs)
