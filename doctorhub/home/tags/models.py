from taggit.models import Tag as TaggitTag
from wagtail.snippets.models import register_snippet


@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy = True
