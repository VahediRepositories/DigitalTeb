class ParentPageMixin:

    @property
    def child_pages(self):
        return [
            child.specific for child in self.get_children().live().public()
        ]
