from django.template.loader import get_template

from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):

    template = get_template(template_src)

    html = template.render(context_dict)

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'attachment; filename="student_result.pdf"'

    pisa.CreatePDF(html, dest=response)

    return response