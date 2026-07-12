import io

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def render_to_pdf(template_name, context):
    template = get_template(template_name)
    html = template.render(context)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode('UTF-8')), result, encoding='UTF-8')

    if pdf.err:
        return HttpResponse('PDF generation error', status=500)

    return HttpResponse(result.getvalue(), content_type='application/pdf')
