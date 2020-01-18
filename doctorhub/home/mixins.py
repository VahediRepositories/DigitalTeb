from wagtail.admin.edit_handlers import MultiFieldPanel, FieldPanel


class ParentPageMixin:

    @property
    def child_pages(self):
        return self.get_children().public().live()


class TaggedPageMixin:
    tags_panel = [
        MultiFieldPanel(
            [
                FieldPanel('rtl_tags'),
            ], heading='RTL Tags', classname='collapsible collapsed'
        ),
        MultiFieldPanel(
            [
                FieldPanel('ltr_tags'),
            ], heading='LTR Tags', classname='collapsible collapsed'
        ),
    ]
