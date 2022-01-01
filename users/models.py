from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.db import models
from events.models import Event
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from .manager import UserManager


GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('NotSay', 'NotSay'),
    ('Other', 'Other'),
)

YEAR_CHOICES = (
    ('1', '1st Year'),
    ('2', '2nd Year'),
    ('3', '3rd Year'),
    ('4', '4th Year'),
    ('5', '5th Year')
)

class CustomUser(AbstractUser):
    username        = None
    email           = models.EmailField(unique=True)
    # password1       = models.CharField(max_length=100, blank=False, null=False, help_text="")
    # password2       = models.CharField(max_length=100, blank=False, null=False, help_text="")
    
    USERNAME_FIELD = 'email'

    objects = UserManager()

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class ExtendedUser(models.Model):
    user                    = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # first_name              = models.CharField(max_length=100, ) 
    events                  = models.ManyToManyField(Event, blank=True, related_name="participants")
    referred_by             = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='referred_users', null=True, blank=True)
    invite_referral         = models.CharField(max_length=8, unique=True, null=True, blank=True, verbose_name='Referral Code for Inviting')
    gender                  = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name='Gender', default='Male')
    contact                 = models.CharField(max_length=10, verbose_name='Contact')
    current_year            = models.CharField(max_length=20, choices=YEAR_CHOICES, verbose_name='Current Year of Study', default='1')
    college                 = models.CharField(max_length=60, verbose_name='College Name')
    city                    = models.CharField(max_length=40, verbose_name='City')
    ambassador              = models.BooleanField(verbose_name='Campus Ambassador', default=False, blank=True)
    isProfileCompleted      = models.BooleanField(verbose_name='Is Profile Completed', default=False, blank=False)

    def __str__(self):
        return self.user.email



@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ExtendedUser.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.extendeduser.save()

