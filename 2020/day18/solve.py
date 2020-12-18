from utils import timeit


@timeit
def get_data():
    data = []
    with open('input.txt') as input_file:
        for line in input_file:
            expression = []
            value = 0
            for c in line:
                if '0' <= c <= '9':
                    value = value * 10 + int(c)
                else:
                    if value > 0:
                        expression.append(value)
                        value = 0
                if c in ('(', ')', '+', '*'):
                    expression.append(c)

            data.append(expression)
    return data


@timeit
def part_1(data):
    def evaluate(expression):
        expression = ['('] + expression
        stack = [')']

        for token in reversed(expression):
            if token == '(':
                while stack[-2] != ')':
                    a = stack.pop()
                    op = stack.pop()
                    b = stack.pop()
                    stack.append(a + b if op == '+' else a * b)
                del stack[-2]
            else:
                stack.append(token)

        return stack[-1]

    return sum(evaluate(expression) for expression in data)


@timeit
def part_2(data):
    def evaluate(expression):
        stack = []
        for token in expression:
            if token == ')':
                exp = []
                while stack[-1] != '(':
                    exp.append(stack.pop())
                stack.pop()
                stack.append(evaluate(exp[::-1]))
            else:
                stack.append(token)
        total = 1
        while len(stack) > 1:
            if stack[-2] == '+':
                a = stack.pop()
                stack.pop()
                b = stack.pop()
                stack.append(a + b)
            else:
                a = stack.pop()
                stack.pop()
                total *= a
        total *= stack.pop()
        assert len(stack) == 0
        return total

    return sum(evaluate(expression) for expression in data)


def main():
    data = get_data()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
