from ..articles.models import *


def get_all_categories():
    return ArticleCategory.objects.all()
