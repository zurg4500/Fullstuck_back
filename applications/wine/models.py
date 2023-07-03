from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime


class Wine(models.Model):
    slug = models.SlugField(primary_key=True, blank=True)
    title= models.CharField(max_length=60)
    excerpt = models.PositiveIntegerField( 
        default=datetime.date.today().year,
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(datetime.date.today().year)
        ]
    )
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    year = models.PositiveIntegerField(
        default=datetime.date.today().year,
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(datetime.date.today().year)
        ]
    )
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="wines"
    )
    quantity = models.PositiveIntegerField()
    in_stock = models.BooleanField(default=False)
    category = models.ForeignKey(
        "category.Category", on_delete=models.CASCADE, related_name="wines"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Wine"
        verbose_name_plural = "Wines"


class WineImage(models.Model):
    wine = models.ForeignKey(
        Wine, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="wine-images")

    def __str__(self):
        return f"{self.pk} to {self.wine.title}"
