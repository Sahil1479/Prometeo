from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from .manager import UserManager


GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other')
)

YEAR_CHOICES = (
    ('first_year', 'First Year'),
    ('second_year', 'Second Year'),
    ('third_year', 'Third Year'),
    ('fourth_year', 'Fourth Year'),
    ('fifth_year', 'Fifth Year')
)

class CustomUser(AbstractUser):
    username        = None
    email           = models.EmailField(unique=True)
    # events        = models.ManyToManyField(Event, blank=True, related_name="participants")
    referred_by     = models.ForeignKey("self", on_delete=models.CASCADE, related_name='referred_users', null=True)
    invite_referral = models.CharField(max_length=8, unique=True, null=True, blank=True, verbose_name='Referral Code for Inviting')
    gender          = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name='Gender', default='male')
    contact         = models.CharField(max_length=10, verbose_name='Contact')
    current_year    = models.CharField(max_length=20, choices=YEAR_CHOICES, verbose_name='Current Year of Study', default='first_year')
    college         = models.CharField(max_length=60, verbose_name='College Name')
    city            = models.CharField(max_length=40, verbose_name='City')
    ambassador      = models.BooleanField(verbose_name='Campus Ambassador', default=False, blank=True)
    
    USERNAME_FIELD = 'email'

    objects = UserManager()

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.first_name
