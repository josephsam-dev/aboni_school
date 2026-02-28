import os
import django
import openpyxl

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth.models import User
from students.models import Student
from parents.models import Parent


workbook = openpyxl.load_workbook("aboni_students.xlsx")
sheet = workbook.active


for row in sheet.iter_rows(min_row=2, values_only=True):

    first_name = row[0]
    last_name = row[1]
    student_class = row[2]
    student_id = row[3]
    parent_name = row[4]
    parent_id = row[5]


    user, created = User.objects.get_or_create(
        username=parent_id,
        defaults={"first_name": parent_name}
    )

    if created:
        user.set_password(parent_id)
        user.save()


    parent, created = Parent.objects.get_or_create(user=user)


    if not Student.objects.filter(student_id=student_id).exists():

        Student.objects.create(
            parent=parent,
            first_name=first_name,
            last_name=last_name,
            student_class=student_class,
            student_id=student_id
        )

        print("Created:", student_id)

    else:

        print("Exists:", student_id)


print("FINISHED")