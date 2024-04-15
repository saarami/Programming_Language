from lexer import INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, ASSIGN, IDENTIFIER, EOF, GREATER, LESS, EQUALS,\
    IF, THEN,ELSE,WHILE,DO,SEMICOLON,LBRACE, RBRACE


class AST:
    pass

class While(AST):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class IfThen(AST):
    def __init__(self, condition, true_stmt):
        self.condition = condition
        self.true_stmt = true_stmt  # true_stmt is now a list of statements

class IfThenElse(AST):
    def __init__(self, condition, true_stmt, false_stmt):
        self.condition = condition
        self.true_stmt = true_stmt  # Both true_stmt and false_stmt are lists
        self.false_stmt = false_stmt


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Parser:
    MAX_STATEMENTS_PER_LINE = 100
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def while_statement(self):
        self.eat(WHILE)  # Consume the 'WHILE' token
        condition = self.expr()  # Parse the condition expression
        self.eat(DO)  # Consume the 'DO' token
        self.eat(LBRACE)  # Consume the opening brace

        body = []
        while self.current_token.type != RBRACE:
            stmt = self.statement()  # Parse one statement within the block
            body.append(stmt)
            if self.current_token.type == SEMICOLON:
                self.eat(SEMICOLON)  # Consume the semicolon and continue
            elif self.current_token.type == RBRACE:
                # If it's right brace, do not eat SEMICOLON, just prepare to end loop
                break
            else:
                # Handle cases where there might be a missing semicolon or other errors
                self.error("Expected SEMICOLON or RBRACE")

        self.eat(RBRACE)  # Consume the closing brace
        return While(condition, body)

    def if_then_statement(self):
        self.eat(IF)  # Consume the 'IF' token
        condition = self.expr()  # Parse the condition expression
        self.eat(THEN)  # Consume the 'THEN' token
        true_stmt = self.statement()  # Parse the true branch statement

        if self.current_token.type == ELSE:  # Check for 'ELSE'
            self.eat(ELSE)
            false_stmt = self.statement()  # Parse the false branch statement
            return IfThenElse(condition, true_stmt, false_stmt)

        return IfThen(condition, true_stmt)

    def comparison(self):
        node = self.term()  # Start with a base non-comparison expression

        while self.current_token.type in (GREATER, LESS, EQUALS):
            token = self.current_token
            self.eat(token.type)  # Consume the comparison operator
            node = BinOp(left=node, op=token, right=self.term())  # Form a comparison expression

        return node

    def error(self, message=None):
        if message:
            raise Exception('Invalid syntax: ' + message)
        else:
            raise Exception('Invalid syntax')

    def eat(self, token_type):
       # print(f"Trying to eat: {token_type}, Current token: {self.current_token.type}")
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f"Expected {token_type}, but got {self.current_token.type}")

    def factor(self):
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            node = self.factor()
            return node
        elif token.type == MINUS:
            self.eat(MINUS)
            node = self.factor()
            return UnaryOp(token, node)
        elif token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        else:
            node = self.variable()
            return node

    def term(self):
        node = self.factor()
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self):
        node = self.term()
        while self.current_token.type in (PLUS, MINUS, GREATER, LESS, EQUALS):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right=self.term())
        return node

    def variable(self):
        node = Var(self.current_token)
        self.eat(IDENTIFIER)
        return node

    def assignment_statement(self):
        # The left side of the assignment (variable name)
        left = self.variable()
        token = self.current_token
        self.eat(ASSIGN)
        # The right side of the assignment (expression/value)
        right = self.expr()
        return Assign(left, token, right)

    def lookahead(self):
        """Peek at the next token without consuming the current token."""
        current_pos = self.lexer.pos
        current_char = self.lexer.current_char
        current_token = self.current_token
        next_token = self.lexer.get_next_token()
        self.lexer.pos = current_pos
        self.lexer.current_char = current_char
        self.lexer.current_token = current_token
        return next_token.type

    def statement_list(self):
        statements = []
        count = 0
        statements.append(self.statement())
        count += 1
        while self.current_token.type == SEMICOLON:
            self.eat(SEMICOLON)
            if self.current_token.type != EOF:
                if count >= self.MAX_STATEMENTS_PER_LINE:
                    raise Exception(
                        f"Error: Exceeded the maximum limit of {self.MAX_STATEMENTS_PER_LINE} commands per line.")
                statements.append(self.statement())
                count += 1
        return statements
    def statement(self):
        if self.current_token.type == IF:
            return self.if_then_statement()
        elif self.current_token.type == WHILE:
            return self.while_statement()
        elif self.current_token.type == IDENTIFIER:
            if self.lookahead() == ASSIGN:
                return self.assignment_statement()
            else:
                return self.expr()
        else:
            return self.expr()



    def parse(self):
        node = self.statement_list()
        if self.current_token.type != EOF:
            self.error()
        return node
