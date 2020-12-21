from collections import defaultdict

import numpy
from utils import timeit


@timeit
def get_data():
    with open('input.txt') as input_file:
        tiles = {}
        current_tile = []
        tile_id = None

        for line in input_file:
            if line.isspace():
                tiles[tile_id] = tuple(current_tile)
                current_tile = []
            elif line.startswith('Tile'):
                tile_id = int(line[5:-2])
            else:
                current_tile.append(line.strip())

        if len(current_tile) > 0:
            tiles[tile_id] = tuple(current_tile)
    return tiles


def get_border_key(border):
    border = border.replace('#', '1').replace('.', '0')
    return min(int(border), int(border[::-1]))


def get_borders(tile):
    top = tile[0]
    bottom = tile[-1]
    left = ''.join(line[0] for line in tile)
    right = ''.join(line[-1] for line in tile)
    return top, bottom, left, right


def get_tiles_matches(tiles):
    borders_tiles = defaultdict(set)
    tiles_borders = {}
    for tile_id, tile in tiles.items():
        borders = get_borders(tile)
        tiles_borders[tile_id] = borders

        for border in borders:
            borders_tiles[get_border_key(border)].add(tile_id)

    tile_matches = defaultdict(set)
    for border, tiles_ in borders_tiles.items():
        if len(tiles_) == 2:
            a, b = tiles_
            tile_matches[a].add(b)
            tile_matches[b].add(a)

    return tile_matches


@timeit
def part_1(tiles):
    tile_matches = get_tiles_matches(tiles)

    total = 1
    for tile_id, matches in tile_matches.items():
        if len(matches) == 2:
            total *= tile_id
    return total


@timeit
def part_2(tiles):
    tile_matches = get_tiles_matches(tiles)

    tiles_ = {}
    for tile_id, tile in tiles.items():
        tile_ = numpy.zeros((len(tile), len(tile[0])), dtype=str)
        for i in range(len(tile)):
            for j in range(len(tile[0])):
                tile_[i, j] = tile[i][j]
        tiles_[tile_id] = tile_
    tiles = tiles_

    def get_match_bottom(tile):
        bottom_border = tiles[tile][-1, :]
        for tile_id in tile_matches[tile]:
            tile_ = tiles[tile_id]
            if (bottom_border == tile_[0, :]).all():
                assert (tiles[tile][-1, :] == tiles[tile_id][0, :]).all()
                return tile_id
            if (bottom_border == tile_[-1, :]).all():
                tiles[tile_id] = numpy.flipud(tile_)
                assert (tiles[tile][-1, :] == tiles[tile_id][0, :]).all()
                return tile_id
            if (bottom_border == tile_[:, 0]).all():
                tiles[tile_id] = numpy.flipud(numpy.rot90(tile_))
                assert (tiles[tile][-1, :] == tiles[tile_id][0, :]).all()
                return tile_id
            if (bottom_border == tile_[:, -1]).all():
                tiles[tile_id] = numpy.rot90(tile_)
                assert (tiles[tile][-1, :] == tiles[tile_id][0, :]).all()
                return tile_id
            if (bottom_border == tile_[0, ::-1]).all():
                tiles[tile_id] = numpy.fliplr(tile_)
                assert (tiles[tile][-1, :] == tiles[tile_id][0, :]).all()
                return tile_id
            if (bottom_border == tile_[-1, ::-1]).all():
                tiles[tile_id] = numpy.rot90(tile_, 2)
                assert (tiles[tile][-1, :] == tiles[tile_id][0, :]).all()
                return tile_id
            if (bottom_border == tile_[::-1, 0]).all():
                tiles[tile_id] = numpy.rot90(tile_, 3)
                assert (tiles[tile][-1, :] == tiles[tile_id][0, :]).all()
                return tile_id
            if (bottom_border == tile_[::-1, -1]).all():
                tiles[tile_id] = numpy.fliplr(numpy.rot90(tile_))
                assert (tiles[tile][-1, :] == tiles[tile_id][0, :]).all()
                return tile_id

    def get_match_right(tile):
        right_border = tiles[tile][:, -1]
        for tile_id in tile_matches[tile]:
            tile_ = tiles[tile_id]
            if (right_border == tile_[:, 0]).all():
                assert (tiles[tile][:, -1] == tiles[tile_id][:, 0]).all()
                return tile_id
            if (right_border == tile_[:, -1]).all():
                tiles[tile_id] = numpy.fliplr(tile_)
                assert (tiles[tile][:, -1] == tiles[tile_id][:, 0]).all()
                return tile_id
            if (right_border == tile_[0, :]).all():
                tiles[tile_id] = numpy.flipud(numpy.rot90(tile_))
                assert (tiles[tile][:, -1] == tiles[tile_id][:, 0]).all()
                return tile_id
            if (right_border == tile_[-1, :]).all():
                tiles[tile_id] = numpy.rot90(tile_, 3)
                assert (tiles[tile][:, -1] == tiles[tile_id][:, 0]).all()
                return tile_id
            if (right_border == tile_[::-1, 0]).all():
                tiles[tile_id] = numpy.flipud(tile_)
                assert (tiles[tile][:, -1] == tiles[tile_id][:, 0]).all()
                return tile_id
            if (right_border == tile_[::-1, -1]).all():
                tiles[tile_id] = numpy.rot90(tile_, 2)
                assert (tiles[tile][:, -1] == tiles[tile_id][:, 0]).all()
                return tile_id
            if (right_border == tile_[0, ::-1]).all():
                tiles[tile_id] = numpy.rot90(tile_)
                assert (tiles[tile][:, -1] == tiles[tile_id][:, 0]).all()
                return tile_id
            if (right_border == tile_[-1, ::-1]).all():
                tiles[tile_id] = numpy.fliplr(numpy.rot90(tile_))
                assert (tiles[tile][:, -1] == tiles[tile_id][:, 0]).all()
                return tile_id

    corners = [tile_id for tile_id, matches in tile_matches.items() if len(matches) == 2]
    corner = corners[0]

    if get_match_bottom(corner) is None:
        tiles[corner] = numpy.flipud(tiles[corner])
    if get_match_right(corner) is None:
        tiles[corner] = numpy.fliplr(tiles[corner])

    puzzle = [[corner]]
    tile = get_match_bottom(corner)
    while tile is not None:
        puzzle.append([tile])
        tile = get_match_bottom(tile)
    for line in puzzle:
        tile = get_match_right(line[0])
        while tile is not None:
            line.append(tile)
            tile = get_match_right(tile)

    height, width = tiles[puzzle[0][0]].shape
    height -= 2
    width -= 2
    image = numpy.zeros((len(puzzle) * height, len(puzzle[0]) * width), dtype=str)

    for i, line in enumerate(puzzle):
        for j, tile in enumerate(line):
            image[i * height:(i + 1) * height, j * width:(j + 1) * width] = tiles[puzzle[i][j]][1:-1, 1:-1]

    monster = numpy.zeros((3, 20), dtype=str)
    with open('monster.txt') as monster_file:
        for i, line in enumerate(monster_file):
            for j, c in enumerate(line[:-1]):
                monster[i, j] = c
    monster[monster != '#'] = '.'

    def search(monster, image):
        height, width = monster.shape
        for i in range(image.shape[0] - height + 1):
            for j in range(image.shape[1] - width + 1):
                view = image[i:i + height, j:j + width]
                if ((monster == '.') | (view != '.')).all():
                    view[monster == '#'] = 'O'

    for _ in range(4):
        search(monster, image)
        monster = numpy.flipud(monster)
        search(monster, image)
        monster = numpy.rot90(numpy.flipud(monster))

    return (image == '#').sum()


def main():
    tiles = get_data()
    part_1(tiles)
    part_2(tiles)


if __name__ == "__main__":
    main()
