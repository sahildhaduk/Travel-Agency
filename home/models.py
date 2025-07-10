from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(null=True, blank=True, upload_to='profile-images/', default='avatar.png')
    # date = models.DateField(default='01-01-2022')

class Contact(models.Model):
    name=models.CharField(max_length=20)
    email=models.CharField(max_length=20)
    message=models.TextField()
    date=models.DateField()

    def __str__(self):
        return self.name

class Register(models.Model):
    username=models.CharField(max_length=20)
    email=models.CharField(max_length=20)
    pass1=models.CharField(max_length=20)
    pass2=models.CharField(max_length=20)
    date=models.DateField()

    def __str__(self):
        return self.username


class Tour(models.Model):
    title = models.CharField(max_length=50, null=False)
    slug = models.CharField(max_length=50, null=False,unique=True)
    description = models.CharField(max_length=1000, null=True)
    price = models.IntegerField(null=False)
    discount = models.IntegerField(null=False, default = 0)
    active = models.BooleanField(default=False)
    thumbnail = models.ImageField(upload_to='tour-images/')
    date = models.DateTimeField(auto_now_add=True)
    day = models.IntegerField(null=True)
    night = models.IntegerField(null=True)
    people = models.IntegerField(null=True)


    def __str__(self):
        return self.title


class TourProperty(models.Model):
    description = models.CharField(max_length=1000, null=False)
    Tour = models.ForeignKey(Tour, null=False, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class Tag(TourProperty):
    pass

class Program(TourProperty):
    pass

class Gallary(models.Model):
    Tour = models.ForeignKey(Tour, null=True, on_delete=models.CASCADE)
    description = models.ImageField(upload_to='Gallary/')

class Subject(models.Model):
    Tour = models.ForeignKey(Tour, null=True, on_delete=models.CASCADE)
    main_description = models.CharField(max_length=200, null=True)
    day_count = models.IntegerField(null=True)
    subj_title = models.CharField(max_length=50, null=False)
    subj_description = models.CharField(max_length=200, null=False)


# ===================== Booking =====================
class TourBooking(models.Model):
    firstname_booking = models.CharField(max_length=20)
    lastname_booking = models.CharField(max_length=20)
    email_booking = models.CharField(max_length=60)
    phone_number = models.CharField(max_length=10)
    check_in = models.DateField(null=True)
    check_out = models.DateField(null=True)
    num_people = models.IntegerField(default=1)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='success')

    def __str__(self):
        return f"{self.firstname_booking} {self.lastname_booking} - {self.tour.title if self.tour else 'No Tour'}"

class Payment(models.Model):
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_session_id = models.CharField(max_length=255)
    status = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - ₹{self.amount} - {self.status}"    