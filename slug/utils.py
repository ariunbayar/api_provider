import random

from main.exceptions import AppError
from .models import (
        SlugGroup,
        SlugEnding,
        SlugGroupEnding,
    )


def unique_slug(namespace, slug):

    group, is_created = SlugGroup.objects.get_or_create(namespace=namespace, slug=slug)

    qs = SlugGroupEnding.objects.filter(group=group)
    pks = qs.values_list('ending_id', flat=True)

    endings = SlugEnding.objects.exclude(pk__in=pks)[:40]

    if not endings.exists():
        raise AppError('E900-2')

    is_slug_used = pks.exists()
    ending = random.choice(endings)
    SlugGroupEnding.objects.create(group=group, ending=ending)

    if not is_slug_used:
        return slug

    return '{}-{}'.format(slug, ending.ending)
