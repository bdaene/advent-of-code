

def solve(data, n=100):
    print(data)
    for i in range(n):
        print(i)
        data = get_unit(fft(data))
        print(data)

    return data


def get_unit(data):
    return tuple(d % 10 if d > 0 else -d % 10 for d in data)


def fft(data):
    sum_data = [0, 0]
    for d in data:
        sum_data.append(sum_data[-1] + d)
    sum_data += [sum_data[-1]] * len(data)

    pattern = (0, 1, 0, -1)
    fs = []
    for k in range(1, len(data)+1):
        f, j = 0, 1
        while k*j <= len(data):
            f += (sum_data[k*(j+1)] - sum_data[k*j]) * pattern[j % 4]
            j += 2
        fs.append(f)

    return fs


if __name__ == "__main__":
    with open('input.txt', 'r') as input_file:
        data = tuple(map(int, input_file.readline().strip()))
    print(''.join(map(str, solve(data)[:8])))
