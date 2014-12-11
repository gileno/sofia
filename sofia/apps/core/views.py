from django.views import generic


index = generic.RedirectView.as_view(
    pattern_name='accounts:dashboard', permanent=False
)
error404 = generic.TemplateView.as_view(template_name='404.html')
error500 = generic.TemplateView.as_view(template_name='500.html')
