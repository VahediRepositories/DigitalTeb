from ...models import *


class ArticlePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticlePage
        fields = [
            'id', 'owner', 'title',
        ]
