from parser import Parser
from interpreter import Interpreter
from lexer import Lexer
MAX_CODE_LENGTH = 1000  # Max number of characters in a single input

def main():
    interpreter = Interpreter(None)  # Assuming Interpreter initialization is correct
    print("Enter commands (Ctrl+D or Ctrl+C to exit):")
    while True:
        try:
            text = input('calc> ')
            if len(text) > MAX_CODE_LENGTH:
                print("Error: Code exceeds maximum allowed length.")
                continue
            if not text:
                continue  # Skip empty inputs

            lexer = Lexer(text)
            parser = Parser(lexer)
            interpreter.parser = parser  # Set the current parser in the interpreter
            result = interpreter.interpret()

            if result is not None and result != []:
                print(result)

        except EOFError:
            print("Exiting...")
            break
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()
