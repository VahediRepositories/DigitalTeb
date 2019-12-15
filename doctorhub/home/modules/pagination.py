from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def get_paginated_objects(request, objects, page_size=5):
    paginator = Paginator(objects, page_size)
    page = request.GET.get('page')
    try:
        paginated_objects = paginator.page(page)
    except PageNotAnInteger:
        paginated_objects = paginator.page(1)
    except EmptyPage:
        paginated_objects = paginator.page(paginator.num_pages)
    return paginated_objects
