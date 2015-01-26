from django.views import generic

from .models import Topic, Reply


class TopicListView(generic.ListView):

    paginate_by = 20
    template_name = 'forum/index.html'

    def get_tag(self):
        return self.kwargs.get('tag', None)

    def get_queryset(self):
        return Topic.objects.all()

    def get_context_data(self, **kwargs):
        context = super(TopicListView, self).get_context_data(**kwargs)
        tags = Topic.tags.all()
        select_sql = '''
        select count(1) from taggit_taggeditem where
        taggit_taggeditem.tag_id=taggit_tag.id
        '''
        tags = tags.extra(select={'count': select_sql}, order_by=['-count'])
        context['tags'] = tags
        return context


index = TopicListView.as_view()
