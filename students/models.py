from django.db import models
from parents.models import Parent


class Student(models.Model):

    parent = models.ForeignKey(
        Parent,
        on_delete=models.CASCADE,
        related_name="children"
    )

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    student_class = models.CharField(max_length=20)

    student_id = models.CharField(max_length=20, unique=True)

    passport = models.CharField(
    max_length=100,
    blank=True,
    null=True
)

    def __str__(self):

        return f"{self.first_name} {self.last_name}"