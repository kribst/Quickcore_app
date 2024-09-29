from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.urls import reverse
from django_countries.fields import CountryField
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password):
        if not email:
            raise ValueError("Vous devez entrer une adresse email")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, username=None, first_name=None, last_name=None):
        user = self.create_user(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_staff = True
        user.is_admin = True
        user.save()
        return user


class CustomerUser(AbstractBaseUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    username = models.CharField(max_length=50, blank=True, null=True, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    country = CountryField(blank_label='(select country)', blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    image = models.ImageField(upload_to='profile_images', null=True, blank=True)
    email = models.EmailField(max_length=50, unique=True, blank=False)

    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @is_staff.setter
    def is_staff(self, value):
        self.is_admin = value

    class Meta:
        ordering = ['first_name', ]


class Stack(models.Model):
    STATUT_CHOICES = [
        ('Done', 'Done'),
        ('Start', 'Start'),
        ('More Time', 'More Time'),
    ]
    title = models.CharField(max_length=1000)
    description = models.TextField()
    image = models.ImageField(upload_to='stack_images', null=True, blank=True)
    duration = models.DateTimeField()
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, related_name='stacks')
    assigned_to = models.ForeignKey(CustomerUser, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='assigned_stacks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=9, choices=STATUT_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['created_at', ]

    def get_absolute_url(self):
        return reverse('stack_detail', kwargs={'pk': self.pk})


class ChatMessage(models.Model):
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.message}"

    class Meta:
        ordering = ['timestamp', ]


# class Visite(models.Model):
#     nombre_de_visiteurs = models.IntegerField(default=0)
#     date_derniere_visite = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return f"Visiteurs: {self.nombre_de_visiteurs}, Dernière mise à jour: {self.date_derniere_visite}"


class Visite(models.Model):
    nombre_de_visiteurs = models.IntegerField(default=0)
    date_derniere_visite = models.DateTimeField(auto_now=True)
    nombre = models.IntegerField(default=0, editable=False)

    def save(self, *args, **kwargs):
        self.nombre = self.nombre_de_visiteurs
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Visiteurs: {self.nombre_de_visiteurs}, Dernière mise à jour: {self.date_derniere_visite}, Nombre: {self.nombre}"