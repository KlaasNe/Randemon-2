from render.SpriteSheetReader import SpriteSheetReader
from render.SpriteSheetReaders import SpriteSheetReaders


class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance


class SpriteSheetWriter(Singleton):

    @staticmethod
    def draw_img(img, render, x, y):
        dest_box = (x, y, x + SpriteSheetReader.TILE_SIZE, y + SpriteSheetReader.TILE_SIZE)
        try:
            # render.paste(image, dest_box, mask=image)
            # except ValueError:
            render.paste(img, dest_box)
        except Exception as e:
            print(e)

    def __init__(self):
        self.readers = dict()
        for reader in SpriteSheetReaders:
            self.readers[reader.name] = reader.value

    def get_tile_img(self, tile):
        return self.readers[tile.reader_name].get_tile(tile.x, tile.y, tile.mirror)

    def draw_tile(self, tile, render, x, y):
        dest_box = (x, y, x + SpriteSheetReader.TILE_SIZE, y + SpriteSheetReader.TILE_SIZE)
        img = self.get_tile_img(tile)
        # render.paste(image, dest_box, mask=image)
        # except ValueError:
        render.paste(img, dest_box)
        return img