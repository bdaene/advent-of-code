from __future__ import annotations
from dataclasses import dataclass
from itertools import islice, chain
from math import prod
from typing import Optional

from utils import timeit


@dataclass
class Packet:
    version: int
    type_id: int
    _value: Optional[int] = None
    packets: tuple[Packet] = ()

    @property
    def version_sum(self):
        return self.version + sum(packet.version_sum for packet in self.packets)

    @property
    def value(self):
        if not self._value:
            if self.type_id == 0:
                self._value = sum(packet.value for packet in self.packets)
            elif self.type_id == 1:
                self._value = prod(packet.value for packet in self.packets)
            elif self.type_id == 2:
                self._value = min(packet.value for packet in self.packets)
            elif self.type_id == 3:
                self._value = max(packet.value for packet in self.packets)
            elif self.type_id == 4:
                pass
            elif self.type_id == 5:
                self._value = 1 if self.packets[0].value > self.packets[1].value else 0
            elif self.type_id == 6:
                self._value = 1 if self.packets[0].value < self.packets[1].value else 0
            elif self.type_id == 7:
                self._value = 1 if self.packets[0].value == self.packets[1].value else 0
        return self._value


def decode(transmission):

    transmission = chain.from_iterable(f'{int(c, 16):04b}' for c in transmission)

    def extract_binary(data, length):
        return int(''.join(islice(data, length)), 2)

    def unpack(data):
        version = extract_binary(data, 3)
        type_id = extract_binary(data, 3)
        packet = Packet(version=version, type_id=type_id)

        if type_id == 4:
            value = 0
            stop = False
            while not stop:
                stop = next(data) == '0'
                value *= 16
                value += extract_binary(data, 4)
            packet._value = value
        else:
            if next(data) == '0':
                total_length = extract_binary(data, 15)
                sub_data = islice(data, total_length)
                packets = []
                while True:
                    try:
                        packets.append(unpack(sub_data))
                    except ValueError:
                        break
                packet.packets = tuple(packets)
            else:
                number_packets = extract_binary(data, 11)
                packet.packets = tuple(unpack(data) for _ in range(number_packets))

        return packet

    return unpack(transmission)


@timeit
def get_data():
    with open('input.txt') as input_file:
        return decode(input_file.readline().strip())


@timeit
def part_1(data):
    return data.version_sum


@timeit
def part_2(data):
    return data.value


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
