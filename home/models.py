from django.db import models

THEME_CHOICES = (
    ('2030', '2030'),
    ('2040', '2040'),
    ('2050', '2050'),
)


class Carousel(models.Model):
    name = models.CharField(max_length=40, blank=True, null=True, verbose_name='Display Name')
    image = models.ImageField(upload_to='carousel_images/', verbose_name='Image to Display in Slide')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Themeimgs(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Display name")
    year = models.CharField(max_length=5, choices=THEME_CHOICES, default='2030')
    image = models.ImageField(upload_to='theme_images/', verbose_name='icons related to theme')

    def __str__(self):
        return self.name