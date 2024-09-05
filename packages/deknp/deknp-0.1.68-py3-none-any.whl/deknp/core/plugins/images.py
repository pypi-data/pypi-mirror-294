import os
from dekmedia.image.svg import trans_image
from .base import Plugin


class PluginImages(Plugin):
    dek_key_images = 'images'

    def run(self):
        images = self.merge_from_key(self.dek_key_images)
        for s, dll in images.items():
            src = os.path.join(self.project_dir, s)
            if os.path.isfile(src):
                if dll:
                    for d, dl in dll.items():
                        if dl is not None:
                            dl = [int(x) for x in dl]
                            sizes = None
                            dpi = None
                            if len(dl) % 2:
                                dpi = int(dl[-1])
                                dl = dl[:-1]
                            if len(dl) > 0:
                                sizes = list(zip(dl[::2], dl[1::2]))
                            trans_image(src, os.path.join(self.project_dir, d), sizes, dpi)
