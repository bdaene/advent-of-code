from itertools import cycle, islice

import numpy
from matplotlib import pyplot
from matplotlib.image import AxesImage
from utils import timeit

ROCKS = """####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
"""


@timeit
def get_data():
    rocks, rock = [], []
    for line in ROCKS.split('\n'):
        if not line:
            rocks.append((numpy.asarray(rock) == '#')[::-1, :])
            rock = []
        else:
            rock.append(list(line.strip()))

    with open('input.txt') as input_file:
        jets = input_file.read().strip()
    return rocks, jets


def simulate(rocks, jets):
    lava_tube = numpy.full((50, 7), False)
    lava_tube[0, :] = True

    jets = [-1 if jet == '<' else 1 for jet in jets]
    jets = cycle(enumerate(jets))
    offset, height = 0, 1
    for r, rock in cycle(enumerate(rocks)):
        h, w = rock.shape
        x, y = 2, height + 3 - offset

        while True:
            j, jet = next(jets)
            new_x = x + jet
            if new_x < 0:
                new_x = 0
            if new_x + w > 7:
                new_x = 7 - w
            if not (lava_tube[y:y + h, new_x:new_x + w] & rock).any():
                x = new_x
            new_y = y - 1
            if (lava_tube[new_y:new_y + h, x:x + w] & rock).any():
                break
            y = new_y

        lava_tube[y:y + h, x:x + w] |= rock
        height = max(height, y + h + offset)
        yield lava_tube, height - 1, r, j, offset
        new_offset = height - lava_tube.shape[0] + 7
        if new_offset > offset:
            delta = new_offset - offset
            offset = new_offset
            lava_tube[:-delta, :] = lava_tube[delta:, :]
            lava_tube[-delta:, :] = False


@timeit
def part_1(rocks, jets, nb_rocks=2022):
    return max(height for _, height, *_ in islice(simulate(rocks, jets), nb_rocks))


@timeit
def part_2(rocks, jets, nb_rocks=1000000000000):
    seen = {}
    heights = [0]
    for n, (lava_tube, height, r, j, _) in enumerate(simulate(rocks, jets), 1):
        key = (r, j, lava_tube.tobytes())
        if key in seen:
            period = n - seen[key]
            height_diff = height - heights[seen[key]]
            d, m = divmod(nb_rocks, period)
            return heights[m] + height_diff * d
        heights.append(height)
        seen[key] = n


def animate(rocks, jets):
    lava_tube = numpy.full((50, 7), False)
    lava_tube[0, :] = True

    image = pyplot.imshow(lava_tube, origin='lower')
    image: AxesImage
    for lava_tube, height, *_, offset in simulate(rocks, jets):
        image.set_data(lava_tube)
        image.set_extent((-.5, lava_tube.shape[1] - .5, offset - .5, offset + lava_tube.shape[0] - .5))
        pyplot.draw()
        pyplot.pause(0.1)


def main():
    rocks, jets = get_data()
    part_1(rocks, jets)
    part_2(rocks, jets)
    animate(rocks, jets)


if __name__ == "__main__":
    main()
