import openpyxl
from django.core.management.base import BaseCommand
from results.models import Result
from students.models import Student


class Command(BaseCommand):

    help = 'Import results from Excel'

    def clean_number(self, value):

        if value is None:
            return 0

        value = str(value).replace("'", "").strip()

        try:
            return int(float(value))
        except:
            return 0


    def handle(self, *args, **kwargs):

        workbook = openpyxl.load_workbook('results.xlsx')
        sheet = workbook.active

        success = 0
        failed = 0
        skipped = 0

        for row in sheet.iter_rows(min_row=2, values_only=True):

            student_id, subject, ca_score, exam_score = row

            if not student_id:
                continue

            ca_score = self.clean_number(ca_score)
            exam_score = self.clean_number(exam_score)

            try:

                student = Student.objects.get(student_id=student_id)

                # check duplicate
                if Result.objects.filter(
                    student=student,
                    subject=subject
                ).exists():

                    skipped += 1

                    self.stdout.write(
                        self.style.WARNING(
                            f"Skipped duplicate: {student_id} - {subject}"
                        )
                    )

                    continue


                Result.objects.create(
                    student=student,
                    subject=subject,
                    ca_score=ca_score,
                    exam_score=exam_score
                )

                success += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Added: {student_id} - {subject}"
                    )
                )


            except Student.DoesNotExist:

                failed += 1

                self.stdout.write(
                    self.style.ERROR(
                        f"Student not found: {student_id}"
                    )
                )


        self.stdout.write("\n====== IMPORT SUMMARY ======")

        self.stdout.write(
            self.style.SUCCESS(f"Added: {success}")
        )

        self.stdout.write(
            self.style.WARNING(f"Skipped: {skipped}")
        )

        self.stdout.write(
            self.style.ERROR(f"Failed: {failed}")
        )