import re

variables = {}
state = {}


def calculate(name):
    if name not in variables:
        raise Exception("INVALID")

    if state.get(name) == "working":
        raise Exception("CYCLE")

    if state.get(name) == "done":
        return variables[name]

    state[name] = "working"
    value = evaluate(variables[name])
    state[name] = "done"
    variables[name] = value
    return value


def evaluate(expression):
    tokens = re.findall(r"\d+|[A-Za-z_][A-Za-z0-9_]*|[()+*-]", expression)
    position = [0]

    def expression_value():
        value = term()
        while position[0] < len(tokens) and tokens[position[0]] in ["+", "-"]:
            op = tokens[position[0]]
            position[0] += 1
            right = term()
            if op == "+":
                value += right
            else:
                value -= right
        return value

    def term():
        value = factor()
        while position[0] < len(tokens) and tokens[position[0]] == "*":
            position[0] += 1
            value *= factor()
        return value

    def factor():
        if position[0] >= len(tokens):
            raise Exception("INVALID")

        token = tokens[position[0]]

        if token.isdigit():
            position[0] += 1
            return int(token)

        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", token):
            position[0] += 1
            return calculate(token)

        if token == "(":
            position[0] += 1
            value = expression_value()
            if position[0] >= len(tokens) or tokens[position[0]] != ")":
                raise Exception("INVALID")
            position[0] += 1
            return value

        raise Exception("INVALID")

    answer = expression_value()

    if position[0] != len(tokens):
        raise Exception("INVALID")

    return answer


def main():
    try:
        n = int(input())

        for i in range(n):
            line = input()
            if "=" not in line:
                raise Exception("INVALID")

            name, expression = line.split("=", 1)
            name = name.strip()
            expression = expression.strip()

            if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
                raise Exception("INVALID")

            variables[name] = expression

        target = input()
        print(evaluate(target))

    except Exception as e:
        print(str(e))


if __name__ == "__main__":
    main()
