from django.shortcuts import render
from django.views.generic import TemplateView


index = TemplateView.as_view(template_name='index.html')
error404 = TemplateView.as_view(template_name='404.html')
error500 = TemplateView.as_view(template_name='500.html')
