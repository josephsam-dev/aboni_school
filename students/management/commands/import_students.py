import os
import django
import openpyxl

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from students.models import Student
from parents.models import Parent


workbook = openpyxl.load_workbook('aboni_students.xlsx')
sheet = workbook.active


for row in sheet.iter_rows(min_row=2, values_only=True):

    first_name = row[0]
    last_name = row[1]
    student_class = row[2]
    student_code = row[3]
    parent_name = row[4]
    parent_code = row[5]


    # create or get parent using phone
    parent, created = Parent.objects.get_or_create(

        phone=parent_code,

        defaults={
            "name": parent_name
        }

    )


    # create student
    Student.objects.create(

        first_name=first_name,
        last_name=last_name,
        student_class=student_class,
        student_id=student_code,
        parent=parent

    )


    print("Created:", first_name, last_name)


print("IMPORT COMPLETE")