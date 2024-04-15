from lexer import INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, ASSIGN, IDENTIFIER, EOF, GREATER, LESS, EQUALS, IF, THEN,\
    ELSE,WHILE,DO,SEMICOLON,LBRACE, RBRACE


MAX_INT = 2**31 - 1  # For 32-bit signed integer maximum
MAX_VARIABLE_COUNT = 50

def check_overflow(result):
    if result > MAX_INT or result < -MAX_INT:
        raise OverflowError("Calculation result exceeds the maximum limit.")
    return result

class NodeVisitor:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def visit_UnaryOp(self, node):
        op_type = node.op.type
        if op_type == MINUS:
            return -self.visit(node.expr)  # Negate the result of the expression
    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.GLOBAL_SCOPE = {}  # Initialize the global scope

    def visit_list(self, nodes):
        result = None
        for node in nodes:
            result = self.visit(node)
        return result

    def visit_While(self, node):
        while self.visit(node.condition):
            self.visit(node.body)

    def visit_IfThen(self, node):
        if self.visit(node.condition):
            return self.visit(node.true_stmt)
        # No 'else' clause to handle

    def visit_IfThenElse(self, node):
        if self.visit(node.condition):
            return self.visit(node.true_stmt)
        else:
            return self.visit(node.false_stmt)

    def visit_BinOp(self, node):
        # Evaluate the left and right subexpressions first
        left = self.visit(node.left)
        right = self.visit(node.right)

        # Check if either subexpression resulted in an error (indicated by None)
        if left is None or right is None:
            return None

        result=0
        # Perform the operation if both subexpressions are valid
        if node.op.type == PLUS:
            result= left + right
        elif node.op.type == MINUS:
            result = left - right
        elif node.op.type == MUL:
            result=  left * right
        elif node.op.type == GREATER:
            return self.visit(node.left) > self.visit(node.right)
        elif node.op.type == LESS:
            return self.visit(node.left) < self.visit(node.right)
        elif node.op.type == EQUALS:
            return self.visit(node.left) == self.visit(node.right)
        elif node.op.type == DIV:
            # Check for division by zero
            if right == 0:
                print("Error: Division by zero.")
                return None
            else:
                result = left // right

        return check_overflow(result)

    def visit_Num(self, node):
        return node.value



    def visit_Var(self, node):
        var_name = node.value
        if var_name in self.GLOBAL_SCOPE:
            return self.GLOBAL_SCOPE[var_name]
        else:
            print(f"Warning: Variable '{var_name}' is not defined.")
            return None  # Optionally return None or continue without returning anything

    def visit_Assign(self, node):
        var_name = node.left.value  # The variable name.
        if var_name not in self.GLOBAL_SCOPE and \
                len(self.GLOBAL_SCOPE) >= MAX_VARIABLE_COUNT:
            raise Exception("Maximum number of variables reached.")
        value = self.visit(node.right)  # Evaluate the right-hand side expression to get its value.
        self.GLOBAL_SCOPE[var_name] = value  # Store the variable and its value in the global scope.
        print(self.GLOBAL_SCOPE)  # Print the current state of the global scope.

    def interpret(self):
        statements = self.parser.parse()  # Should return a list of statements
        results = []
        for statement in statements:
            result = self.visit(statement)
            if result is not None:
                results.append(result)
        return results