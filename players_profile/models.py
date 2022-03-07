from django.db import models

from authentication.models import User


class Profile(models.Model):
    SURFACES = (
        ('CLAY', 'clay'),
        ('HARD', 'hard'),
        ('GRASS', 'grass'),
    )

    GENDERS = (
        ('FEMALE', 'female'),
        ('MALE', 'male'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=True, default="")
    surname = models.CharField(max_length=30, blank=True, default="")
    age = models.PositiveSmallIntegerField(null=True)
    gender = models.CharField(choices=GENDERS, max_length=20, blank=True)
    racquet = models.CharField(max_length=20, blank=True, default="")
    city = models.CharField(max_length=30, blank=True, default="")
    favorite_surface = models.CharField(choices=SURFACES, max_length=20, blank=True)
    nrtp = models.FloatField(blank=True, null=True)

    def is_complete(self):
        if all((self.name, self.surname, self.age, self.gender, self.city)):
            return True
        else:
            return False

    def __str__(self):
        if self.is_complete():
            return f"{self.name} {self.surname} ({self.gender}, {self.age}) from {self.city}"
        else:
            return self.user.email

