

def solve(data, n, index):
    data = data[index:]
    for i in range(n):
        fft = []
        s = 0
        for d in reversed(data):
            s = (s + d) % 10
            fft.append(s)
        data = fft[::-1]
    return data[:8]


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        data = tuple(map(int, input_file.readline().strip()))
    # data = tuple(map(int, "03036732577212944063491565474664"))
    data *= 10000
    index = int(''.join(map(str, data[:7])))

    assert(index > len(data)//2)
    print(index)
    print(len(data)-index+1)
    print(''.join(map(str, solve(data, 100, index))))
