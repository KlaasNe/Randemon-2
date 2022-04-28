from enum import Enum

from mapClasses import Tile


def create_edges(chunk, hill_type=0):
    remove_faulty_heights(chunk)
    create_hill_edges(chunk, hill_type)


def remove_faulty_heights(chunk):
    for y in range(chunk.size):
        prev_surrounding = None
        for x in range(chunk.size):
            prev_surrounding = get_surrounding_tiles(chunk, x, y, prev_surrounding)
            height_change = get_tile_from_surrounding(prev_surrounding, FaultyHillTiles)
            if height_change is not None:
                chunk.change_height(x, y, height_change)
            else:
                prev_surrounding = None


def create_hill_edges(chunk, hill_type):
    for y in range(chunk.size):
        prev_surrounding = None
        for x in range(chunk.size):
            if chunk.get_height(x, y) > 1:
                prev_surrounding = get_surrounding_tiles(chunk, x, y, prev_surrounding)
                height_change = get_tile_from_surrounding(prev_surrounding, HillTiles)
                if isinstance(height_change, Tile):
                    chunk.set_tile("HILLS", x, y, HillTiles.specific_tile(height_change, hill_type))
                else:
                    if height_change == "lower":
                        chunk.change_height(x, y, -1)
                    elif height_change == "higher":
                        chunk.change_height(x, y, 1)
                    prev_surrounding = None
            else:
                prev_surrounding = None


def get_surrounding_tiles(chunk, x, y, prev):
    curr_h = chunk.get_height(x, y)
    if prev is None:
        return [[chunk.get_height(hx, hy) - curr_h for hx in range(x - 1, x + 2)] for hy in range(y - 1, y + 2)]
    else:
        new = [r[1:] for r in prev]
        for hy in range(3):
            new[hy].append(chunk.get_height(x + 1, y - 1 + hy) - curr_h)
        return new


def get_tile_from_surrounding(surrounding, tile_enum):
    for tile in tile_enum:
        if equal_surrounding(tile.value[0], surrounding):
            return tile.value[1]


def equal_surrounding(template, arr):
    if arr is not None:
        for y in range(3):
            for x in range(3):
                if template[y][x] is not None and template[y][x] != arr[y][x]:
                    return False
    return True


class HillTiles(Enum):

    @staticmethod
    def specific_tile(tile, tile_type):
        return Tile("HILLS", tile.x + tile_type * 5, tile.y)

    A = [[None, None, None], [0, 0, None], [-1, 0, None]], Tile("HILLS", 0, 1)
    B = [[None, None, None], [None, 0, 0], [None, 0, -1]], Tile("HILLS", 0, 2)
    C1 = [[-1, 0, None], [0, 0, None], [None, None, None]], Tile("HILLS", 3, 0)
    C2 = [[None, 0, -1], [None, 0, 0], [None, None, None]], Tile("HILLS", 3, 0)
    E = [[None, 0, None], [-1, 0, 0], [None, 0, None]], Tile("HILLS", 1, 0)
    F = [[None, 0, None], [0, 0, 0], [None, -1, None]], Tile("HILLS", 4, 0)
    G = [[None, 0, None], [0, 0, -1], [None, 0, None]], Tile("HILLS", 2, 0)
    H = [[None, -1, None], [0, 0, 0], [None, 0, None]], Tile("HILLS", 3, 0)
    I = [[None, -1, None], [-1, 0, 0], [None, 0, None]], Tile("HILLS", 1, 1)
    J = [[None, 0, None], [-1, 0, 0], [None, -1, None]], Tile("HILLS", 3, 1)
    K = [[None, 0, None], [0, 0, -1], [None, -1, None]], Tile("HILLS", 4, 1)
    L = [[None, -1, None], [0, 0, -1], [None, 0, None]], Tile("HILLS", 2, 1)


class FaultyHillTiles(Enum):

    X1 = [[None, -1, None], [None, 0, None], [None, -1, None]], -1
    X2 = [[None, 1, None], [None, 0, None], [None, 1, None]], 1
    X3 = [[None, None, None], [-1, 0, -1], [None, None, None]], -1
    X4 = [[None, None, None], [1, 0, 1], [None, None, None]], 1
