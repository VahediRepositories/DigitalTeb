from wagtail.admin.edit_handlers import MultiFieldPanel, FieldPanel


class ParentPageMixin:

    @property
    def child_pages(self):
        return [
            child.specific for child in self.get_children().live().public().order_by(
                '-first_published_at'
            )
        ]


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
