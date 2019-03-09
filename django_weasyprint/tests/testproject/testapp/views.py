from django_weasyprint import views


class Sample1View(views.WeasyTemplateView):
    template_name = 'sample1.html'
