from ..modules import images


class CompressingImageMixin:
    def compress_image(self):
        if self.image:
            images.compress_image(self.image.path)


class SquareIconMixin(CompressingImageMixin):
    def make_square_image(self):
        if self.image:
            images.make_square_image(self.image.path)
