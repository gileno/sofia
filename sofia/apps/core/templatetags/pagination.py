from django.conf import settings
from django import template


register = template.Library()

DEFAULT_WINDOW = getattr(settings, 'PAGINATION_DEFAULT_WINDOW', 4)


@register.inclusion_tag(file_name='paginate.html', takes_context=True)
def paginate(context, anchor=None, window=DEFAULT_WINDOW):
    """
    Renders the ``pagination/pagination.html`` template, resulting in a
    Digg-like display of the available pages, given the current page.  If there
    are too many pages to be displayed before and after the current page, then
    elipses will be used to indicate the undisplayed gap between page numbers.
    Requires one argument, ``context``, which should be a dictionary-like data
    structure and must contain the following keys:
    ``paginator``
        A ``Paginator`` or ``QuerySetPaginator`` object.
    ``page_obj``
        This should be the result of calling the page method on the
        aforementioned ``Paginator`` or ``QuerySetPaginator`` object, given
        the current page.
    This same ``context`` dictionary-like data structure may also include:
    ``getvars``
        A dictionary of all of the **GET** parameters in the current request.
        This is useful to maintain certain types of state, even when requesting
        a different page.
    """
    try:
        paginator = context['paginator']
        page_obj = context['page_obj']
        page_range = paginator.page_range
        first = set([1])
        last = set([paginator.num_pages])
        current_start = page_obj.number - 1 - window
        if current_start < 0:
            current_start = 0
        current_end = page_obj.number - 1 + window
        if current_end < 0:
            current_end = 0
        current = set(page_range[current_start:current_end])
        pages = []
        if len(first.intersection(current)) == 0:
            first_list = list(first)
            first_list.sort()
            second_list = list(current)
            second_list.sort()
            pages.extend(first_list)
            diff = second_list[0] - first_list[-1]
            if diff == 2:
                pages.append(second_list[0] - 1)
            elif diff == 1:
                pass
            else:
                pages.append(None)
            pages.extend(second_list)
        else:
            unioned = list(first.union(current))
            unioned.sort()
            pages.extend(unioned)
        if len(current.intersection(last)) == 0:
            second_list = list(last)
            second_list.sort()
            diff = second_list[0] - pages[-1]
            if diff == 2:
                pages.append(second_list[0] - 1)
            elif diff == 1:
                pass
            else:
                pages.append(None)
            pages.extend(second_list)
        else:
            differenced = list(last.difference(current))
            differenced.sort()
            pages.extend(differenced)
        to_return = {
            'MEDIA_URL': settings.MEDIA_URL,
            'pages': pages,
            'page_obj': page_obj,
            'paginator': paginator,
            'is_paginated': paginator.count > paginator.per_page,
            'anchor': anchor,
        }
        if 'request' in context:
            getvars = context['request'].GET.copy()
            if 'page' in getvars:
                del getvars['page']
            if len(getvars.keys()) > 0:
                to_return['getvars'] = "&%s" % getvars.urlencode()
            else:
                to_return['getvars'] = ''
        return to_return
    except (KeyError, AttributeError):
        return {}
