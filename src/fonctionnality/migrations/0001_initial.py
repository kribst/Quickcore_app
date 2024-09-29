# Generated by Django 5.1 on 2024-09-13 16:19

import django.db.models.deletion
import django_countries.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CustomerUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "username",
                    models.CharField(blank=True, max_length=50, null=True, unique=True),
                ),
                ("first_name", models.CharField(blank=True, max_length=30)),
                ("last_name", models.CharField(blank=True, max_length=30)),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[("M", "Male"), ("F", "Female"), ("O", "Other")],
                        max_length=1,
                        null=True,
                    ),
                ),
                (
                    "country",
                    django_countries.fields.CountryField(blank=True, max_length=2),
                ),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="profile_images"
                    ),
                ),
                ("email", models.EmailField(max_length=50, unique=True)),
                ("is_admin", models.BooleanField(default=False)),
            ],
            options={
                "ordering": ["first_name"],
            },
        ),
        migrations.CreateModel(
            name="Visite",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre_de_visiteurs", models.IntegerField(default=0)),
                ("date_derniere_visite", models.DateTimeField(auto_now=True)),
                ("nombre", models.IntegerField(default=0, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name="ChatMessage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("message", models.TextField()),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["timestamp"],
            },
        ),
        migrations.CreateModel(
            name="Stack",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=1000)),
                ("description", models.TextField()),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="stack_images"),
                ),
                ("duration", models.DateTimeField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Done", "Done"),
                            ("Start", "Start"),
                            ("More Time", "More Time"),
                        ],
                        max_length=9,
                        null=True,
                    ),
                ),
                (
                    "assigned_to",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="assigned_stacks",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="stacks",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["created_at"],
            },
        ),
    ]
