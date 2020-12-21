from collections import defaultdict

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


def get_tiles_matches(tiles):
    def get_key(border):
        border = ''.join(border).replace('.', '0').replace('#', '1')
        return min(int(border), int(border[::-1]))

    borders_tiles = defaultdict(set)
    for tile_id, tile in tiles.items():
        borders_tiles[get_key(tile[0, :])].add(tile_id)
        borders_tiles[get_key(tile[-1, :])].add(tile_id)
        borders_tiles[get_key(tile[:, 0])].add(tile_id)
        borders_tiles[get_key(tile[:, -1])].add(tile_id)

    tile_matches = defaultdict(set)
    for matching_tiles in borders_tiles.values():
        for tile in sorted(matching_tiles):
            matching_tiles.remove(tile)
            for tile_ in matching_tiles:
                tile_matches[tile].add(tile_)
                tile_matches[tile_].add(tile)

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

    def gen_orientations(tile):
        for _ in range(4):
            yield tile
            yield numpy.flipud(tile)
            tile = numpy.rot90(tile)

    def get_match_bottom(tile_id):
        tile = tiles[tile_id]
        for tile_id_ in tile_matches[tile_id]:
            tile_ = tiles[tile_id_]
            for orientation in gen_orientations(tile_):
                if (tile[-1, :] == orientation[0, :]).all():
                    tiles[tile_id_] = orientation
                    return tile_id_

    def get_match_right(tile_id):
        tile = tiles[tile_id]
        for tile_id_ in tile_matches[tile_id]:
            tile_ = tiles[tile_id_]
            for orientation in gen_orientations(tile_):
                if (tile[:, -1] == orientation[:, 0]).all():
                    tiles[tile_id_] = orientation
                    return tile_id_

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

    monster = numpy.full((3, 20), ' ')
    monster[0, :] = tuple('                  # ')
    monster[1, :] = tuple('#    ##    ##    ###')
    monster[2, :] = tuple(' #  #  #  #  #  #   ')

    def search(monster, image):
        height, width = monster.shape
        for i in range(image.shape[0] - height + 1):
            for j in range(image.shape[1] - width + 1):
                view = image[i:i + height, j:j + width]
                if ((monster != '#') | (view == '#')).all():
                    view[monster == '#'] = 'O'

    for orientation in gen_orientations(monster):
        search(orientation, image)

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
