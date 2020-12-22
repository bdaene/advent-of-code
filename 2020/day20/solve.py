from collections import defaultdict, Counter

import numpy
from matplotlib import pyplot
from utils import timeit


@timeit
def get_data(tile_size=10):
    with open('input.txt') as input_file:
        tiles = {}
        current_tile = numpy.full((tile_size, tile_size), '.')
        row = 0
        tile_id = None

        for line in input_file:
            if line.isspace():
                tiles[tile_id] = current_tile
                current_tile = numpy.full((tile_size, tile_size), '.')
                row = 0
            elif line.startswith('Tile'):
                tile_id = int(line[5:-2])
            else:
                current_tile[row, :] = tuple(line.strip())
                row += 1

        if row == tile_size:
            tiles[tile_id] = current_tile
    return tiles


def get_key(border):
    border = ''.join(border).replace('.', '0').replace('#', '1')
    return min(int(border), int(border[::-1]))


def get_borders(tiles):
    borders_tiles = defaultdict(set)
    for tile_id, tile in tiles.items():
        borders_tiles[get_key(tile[0, :])].add(tile_id)
        borders_tiles[get_key(tile[-1, :])].add(tile_id)
        borders_tiles[get_key(tile[:, 0])].add(tile_id)
        borders_tiles[get_key(tile[:, -1])].add(tile_id)
    return borders_tiles


def gen_corners(borders_tiles):
    adjacent_tiles_count = Counter()

    for tiles in borders_tiles.values():
        for tile in tiles:
            adjacent_tiles_count[tile] += len(tiles) - 1

    for tile_id, count in adjacent_tiles_count.items():
        if count == 2:
            yield tile_id


@timeit
def part_1(tiles):
    borders_tiles = get_borders(tiles)

    total = 1
    for tile_id in gen_corners(borders_tiles):
        total *= tile_id
    return total


@timeit
def part_2(tiles):
    borders_tiles = get_borders(tiles)

    def gen_orientations(tile):
        for _ in range(4):
            yield tile
            yield numpy.flipud(tile)
            tile = numpy.rot90(tile)

    def get_match_bottom(tile_id):
        bottom_border = tiles[tile_id][-1, :]
        try:
            adjacent_tile_id = tuple(borders_tiles[get_key(bottom_border)] - {tile_id})[0]
        except IndexError:
            return None
        adjacent_tile = tiles[adjacent_tile_id]
        for orientation in gen_orientations(adjacent_tile):
            if (bottom_border == orientation[0, :]).all():
                tiles[adjacent_tile_id] = orientation
                return adjacent_tile_id

    def get_match_right(tile_id):
        right_border = tiles[tile_id][:, -1]
        try:
            adjacent_tile_id = tuple(borders_tiles[get_key(right_border)] - {tile_id})[0]
        except IndexError:
            return None
        adjacent_tile = tiles[adjacent_tile_id]
        for orientation in gen_orientations(adjacent_tile):
            if (right_border == orientation[:, 0]).all():
                tiles[adjacent_tile_id] = orientation
                return adjacent_tile_id

    corner = next(gen_corners(borders_tiles))

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

    monster = ['                  # ',
               '#    ##    ##    ###',
               ' #  #  #  #  #  #   ']
    monster_coord = tuple(
        (row, col) for row, line in enumerate(monster) for col, cell in enumerate(line) if cell == '#')

    # for orientation in (numpy.rot90(image, 3),):
    for orientation in gen_orientations(image):
        for row in range(orientation.shape[0] - 2):
            for col in range(orientation.shape[1] - 19):
                if all(orientation[row + r, col + c] != '.' for r, c in monster_coord):
                    for r, c in monster_coord:
                        orientation[row + r, col + c] = 'O'

    image = numpy.rot90(image, 3)
    image_ = numpy.zeros(image.shape + (3,), dtype=numpy.uint8)
    image_[image == '.', :] = (0, 127, 255)
    image_[image == '#', :] = (0, 63, 127)
    image_[image == 'O', :] = (255, 0, 0)
    pyplot.imshow(image_)
    pyplot.show()

    return (image == '#').sum()


def main():
    tiles = get_data()
    part_1(tiles)
    part_2(tiles)


if __name__ == "__main__":
    main()
