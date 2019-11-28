from django.db import models


class SlugGroup(models.Model):

    namespace = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, allow_unicode=True)


class SlugEnding(models.Model):

    ending = models.CharField(max_length=10, unique=True)


class SlugGroupEnding(models.Model):

    group = models.ForeignKey(SlugGroup, on_delete=models.PROTECT)
    ending = models.ForeignKey(SlugEnding, on_delete=models.PROTECT)
