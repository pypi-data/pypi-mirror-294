from django.db import models
from django.db.models import functions
from django.contrib.auth import get_user_model


User = get_user_model()


class AuthorManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                full_name=functions.Concat(
                    "first_name",
                    models.Value(" "),
                    "last_name",
                    output_field=models.CharField(),
                ),
            )
        )


class ContainsAManager(AuthorManager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                models.Q(full_name__contains="A") | models.Q(full_name__contains="a")
            )
            .annotate(
                a_count=models.ExpressionWrapper(
                    functions.Length("full_name")
                    - functions.Length(
                        functions.Replace(
                            functions.Replace("full_name", models.Value("A")),
                            models.Value("a"),
                        )
                    ),
                    output_field=models.PositiveIntegerField(),
                )
            )
        )


class Author(models.Model):
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16)
    user = models.ForeignKey(User, models.CASCADE, null=True)

    objects = AuthorManager()
    contains_a = ContainsAManager()
