from rest_framework.fields import Field
from wagtail.images.api.fields import ImageRenditionField


class ParagraphField(Field):
    def to_internal_value(self, data):
        pass

    def to_representation(self, paragraph):
        value = paragraph.value
        paragraph = value['paragraph']
        dic = {
            'paragraph': paragraph.source,
        }
        keys = value.keys()
        if 'title' in keys:
            dic['title'] = value['title']
        if 'image' in keys:
            dic['image'] = ImageRenditionField('fill-2000x2000-c80|jpegquality-100').to_representation(value['image'])
        return dic


class ParagraphsField(Field):
    def to_internal_value(self, data):
        pass

    def to_representation(self, paragraphs):
        return [
            ParagraphField().to_representation(paragraph)
            for paragraph in paragraphs
        ]


class ArticleCategoriesField(Field):
    def to_internal_value(self, data):
        pass

    def to_representation(self, categories):
        return [
            {
                'farsi_name': category.farsi_name,
                'english_name': category.english_name,
            } for category in categories.all()
        ]
