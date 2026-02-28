from django.urls import path
from . import views

urlpatterns = [

    path('student-results/', views.student_results, name='student_results'),

    path('<int:student_id>/', views.parent_result, name='parent_result'),
    path('result-pdf/<int:student_id>/', views.download_result_pdf, name="result_pdf"),

]