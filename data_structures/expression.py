class ExpressionStack:
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if len(self.stack) == 0:
            return None

        return self.stack.pop()


def evaluate_postfix(expression):
    stack = ExpressionStack()

    tokens = expression.split()

    for token in tokens:

        if token.isdigit() or token.replace(".", "", 1).isdigit():
            stack.push(float(token))

        elif token in "+-*/":

            if len(stack.stack) < 2:
                return None

            b = stack.pop()
            a = stack.pop()

            if token == "+":
                result = a + b

            elif token == "-":
                result = a - b

            elif token == "*":
                result = a * b

            elif token == "/":
                if b == 0:
                    return None
                result = a / b

            stack.push(result)

        else:
            return None

    if len(stack.stack) == 1:
        return stack.pop()

    return None