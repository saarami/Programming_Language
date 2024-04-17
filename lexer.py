import re

# Token types
INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, ASSIGN, IDENTIFIER, EOF, GREATER, LESS, EQUALS ,\
    IF, THEN ,ELSE,WHILE,DO,SEMICOLON,LBRACE, RBRACE= (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', 'LPAREN', 'RPAREN', 'ASSIGN', 'IDENTIFIER', 'EOF', 'GREATER', 'LESS',
    'EQUALS','IF', 'THEN','ELSE','WHILE','DO','SEMICOLON','LBRACE', 'RBRACE'
)


class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self, message):
        raise Exception(f"Lexer error: {message}")

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def _id(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalpha()):
            result += self.current_char
            self.advance()

        # Validate the length of the identifier
        if len(result) > 4 and result not in ('if', 'then', 'else', 'while', 'do'):
            self.error("Identifier names can only be up to 4 letters long.")

        # Mapping keywords to their specific token types
        keyword_map = {
            'if': IF,
            'then': THEN,
            'else': ELSE,
            'while': WHILE,
            'do': DO
        }

        token_type = keyword_map.get(result, IDENTIFIER)  # Defaults to IDENTIFIER if not a keyword
        return Token(token_type, result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return self.integer()

            if self.current_char.isalpha() or self.current_char == '_':  # Start of identifier or keyword
                return self._id()

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_char == '>':
              #  print("Handling '>' character")
                self.advance()
                return Token(GREATER, '>')

            if self.current_char == '<':
                self.advance()
                return Token(LESS, '<')

            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':  # Checking for equality operator '=='
                    self.advance()
                    return Token(EQUALS, '==')
                return Token(ASSIGN, '=')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == ';':
                self.advance()
                return Token(SEMICOLON, ';')

            if self.current_char == '{':
                self.advance()
                return Token(LBRACE, '{')

            if self.current_char == '}':
                self.advance()
                return Token(RBRACE, '}')

            # Error handling
            return Token('ERROR', None)


        return Token(EOF, None)


    def integer(self):
        """ Retrieve a full integer from the input (part of the lexer). """
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return Token(INTEGER, int(result))  # Ensure that a Token object is returned
