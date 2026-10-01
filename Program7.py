import re


class InvalidFormatError(Exception):
    pass


class UnknownVariableError(Exception):
    pass


class DivisionByZeroError(Exception):
    pass


class UnsupportedOperatorError(Exception):
    pass


def get_value(value, variables):
    if re.fullmatch(r"[+-]?(\d+(\.\d*)?|\.\d+)", value):
        return float(value) if "." in value else int(value)

    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", value):
        if value not in variables:
            raise UnknownVariableError()
        return variables[value]

    raise InvalidFormatError()


def calculate(line, variables):
    parts = line.split()

    if len(parts) != 3:
        raise InvalidFormatError()

    left, operator, right = parts

    if operator not in ["+", "-", "*", "/", "%"]:
        raise UnsupportedOperatorError()

    a = get_value(left, variables)
    b = get_value(right, variables)

    if operator in ["/", "%"] and b == 0:
        raise DivisionByZeroError()

    if operator == "+":
        return a + b
    if operator == "-":
        return a - b
    if operator == "*":
        return a * b
    if operator == "/":
        return a / b
    return a % b


def show(value):
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def main():
    variables = {}

    while True:
        try:
            line = input().strip()
        except EOFError:
            break

        if line.lower() == "quit":
            break

        try:
            if "=" in line:
                if line.count("=") != 1:
                    raise InvalidFormatError()

                name, expression = line.split("=")
                name = name.strip()
                expression = expression.strip()

                if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
                    raise InvalidFormatError()

                if len(expression.split()) == 1:
                    variables[name] = get_value(expression, variables)
                else:
                    variables[name] = calculate(expression, variables)

            else:
                result = calculate(line, variables)
                print(show(result))

        except DivisionByZeroError:
            print("DivisionByZeroError")
        except UnsupportedOperatorError:
            print("UnsupportedOperatorError")
        except UnknownVariableError:
            print("UnknownVariableError")
        except InvalidFormatError:
            print("InvalidFormatError")


if __name__ == "__main__":
    main()
