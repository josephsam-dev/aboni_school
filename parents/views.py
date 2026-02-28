from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Parent
from students.models import Student


@login_required
def parent_dashboard(request):

    try:
        parent = Parent.objects.get(user=request.user)
    except Parent.DoesNotExist:
        return redirect("/accounts/login/")

    students = Student.objects.filter(parent=parent)

    return render(request, "parents/dashboard.html", {

        "parent": parent,
        "students": students

    })