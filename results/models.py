from django.db import models
from students.models import Student


class Subject(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Result(models.Model):

    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    subject = models.CharField(max_length=100)

    ca_score = models.IntegerField(default=0)

    exam_score = models.IntegerField(default=0)

    total_score = models.IntegerField(default=0)

    grade = models.CharField(max_length=2, blank=True)

    # Teacher comment
    teacher_comment = models.CharField(max_length=200, blank=True)

    # Principal signature (temporarily CharField for deployment safety)
    principal_signature = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )


    def __str__(self):

        return f"{self.student.first_name} {self.student.last_name} - {self.subject} - {self.total_score}"


    def save(self, *args, **kwargs):

        self.total_score = self.ca_score + self.exam_score

        if self.total_score >= 70:
            self.grade = "A"

        elif self.total_score >= 60:
            self.grade = "B"

        elif self.total_score >= 50:
            self.grade = "C"

        elif self.total_score >= 45:
            self.grade = "D"

        elif self.total_score >= 40:
            self.grade = "E"

        else:
            self.grade = "F"

        super().save(*args, **kwargs)