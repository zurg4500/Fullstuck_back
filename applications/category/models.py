from django.db import models
from slugify import slugify


class Category(models.Model):
    slug = models.SlugField(primary_key=True, blank=True)
    title = models.CharField(unique=True, max_length=100)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
