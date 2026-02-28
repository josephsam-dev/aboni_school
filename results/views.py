from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from students.models import Student
from .models import Result
from .utils import render_to_pdf
# ============================================
# VIEW ALL RESULTS (OPTIONAL - ADMIN USE)
# ============================================

@login_required
def student_results(request):

    results = Result.objects.all()

    return render(request, "results/student_results.html", {

        "results": results

    })


# ============================================
# SECURE PARENT RESULT VIEW
# ============================================

@login_required
def parent_result(request, student_id):

    student = get_object_or_404(Student, id=student_id)

    # 🔒 SECURITY CHECK
    if student.parent.user != request.user:

        return render(request, "results/access_denied.html")


    results = Result.objects.filter(student=student)


    # =====================
    # CALCULATE AVERAGE
    # =====================

    total = sum(result.total_score for result in results)

    count = results.count()

    average = 0

    if count > 0:

        average = round(total / count, 2)


    # =====================
    # CALCULATE POSITION
    # =====================

    students = Student.objects.all()

    totals = []

    for s in students:

        s_results = Result.objects.filter(student=s)

        s_total = sum(r.total_score for r in s_results)

        totals.append((s, s_total))


    totals.sort(key=lambda x: x[1], reverse=True)


    position = 0

    for index, item in enumerate(totals):

        if item[0].id == student.id:

            position = index + 1

            break


    total_students = len(totals)


    return render(request, "results/result.html", {

        "student": student,
        "results": results,
        "average": average,
        "position": position,
        "total_students": total_students,

    })


# ============================================
# DOWNLOAD RESULT PDF
# ============================================

@login_required
def download_result_pdf(request, student_id):

    student = get_object_or_404(Student, id=student_id)

    # 🔒 SECURITY CHECK
    if student.parent.user != request.user:

        return render(request, "results/access_denied.html")


    results = Result.objects.filter(student=student)


    total = sum(result.total_score for result in results)

    count = results.count()

    average = 0

    if count > 0:

        average = round(total / count, 2)


    pdf = render_to_pdf("results/result.html", {

        "student": student,
        "results": results,
        "average": average,
        "position": "",
        "total_students": "",

    })


    return HttpResponse(pdf, content_type='application/pdf')