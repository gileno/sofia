from django.views import generic


class IndexView(generic.RedirectView):

    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            self.pattern_name = 'accounts:dashboard'
        else:
            self.pattern_name = 'learn:project_list'
        return super(IndexView, self).get_redirect_url(*args, **kwargs)


index = IndexView.as_view()
error404 = generic.TemplateView.as_view(template_name='404.html')
error500 = generic.TemplateView.as_view(template_name='500.html')
