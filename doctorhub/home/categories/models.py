from django.db import models
from django.forms import TextInput
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, FieldRowPanel


class Category(models.Model):
    farsi_name = models.TextField()
    english_name = models.TextField()
    name = models.TextField(default='')

    panels = [
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel('name_en_us', widget=TextInput),
                        FieldPanel('name_fa_ir', widget=TextInput),
                    ]
                ),
            ], heading='Name', classname="collapsible collapsed"
        ),

        FieldPanel('farsi_name'),
        FieldPanel('english_name'),
    ]

    def __str__(self):
        return self.farsi_name

    class Meta:
        abstract = True
