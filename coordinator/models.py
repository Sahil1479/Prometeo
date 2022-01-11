from django.db import models

# Create your models here.

TEAM_CHOICES = (
    ("Web Development", "Web Development"),
    ("Marketing", "Marketing"),
    ("Public Relations", "Public Relations"),
    ("Resourse Management", "Resourse Management"),
    ("Technical Events", "Technical Events"),
    ("TedX", "TedX"),
    ("Entrepreneur", "Entrepreneur"),
    ("Services", "Services"),
    ("Media", "Media"),
    ("Exhibition", "Exhibition"),
    ("Pronite", "Pronite"),
    ("Informals", "Informals"),
    ("Design and Creativity", "Design and Creativity"),
)


class Designation(models.Model):
    designationName = models.CharField(max_length=100, blank=False, null=False)
    rank = models.IntegerField(blank=False, null=False, default=1)

    def __str__(self):
        return self.designationName


class Coordinator(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    team = models.ForeignKey(Designation, on_delete=models.CASCADE)
    # category = models.CharField(max_length=100, choices=CHOICE_CATEGORY)
    image = models.ImageField(upload_to="uploads/team/")
    github_link = models.URLField(max_length=1000, blank=True, null=True)
    instagram_link = models.URLField(max_length=1000, blank=True, null=True)
    facebook_link = models.URLField(max_length=1000, blank=True, null=True)
    linkedin_link = models.URLField(max_length=1000, blank=True, null=True)
    email = models.CharField(max_length=100, blank=False, null=False)
    phoneNo = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return f"{self.name} [{self.team}]"


