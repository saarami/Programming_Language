# Programming_Language_Project

## Overview
This project explores the design and implementation of a basic programming language interpreter. It focuses on fundamental programming constructs like variable assignment, arithmetic operations, and control structures such as conditional statements and loops.

## Features
- **Variable Assignment**: Supports integers with simple assignment operations.
- **Arithmetic Operations**: Includes addition, subtraction, multiplication, and division.
- **Control Structures**: Implements `if-then`, `if-then-else`, and `while-do` statements, allowing for complex flow control.
- **Memory Management**: Enforces limits on the number of variables, program length, and calculation values to prevent overflow and ensure efficient memory use.

## Getting Started
### Prerequisites
- Python 3.8 or above
  
Enter expressions at the `calc>` prompt. To exit, use `Ctrl+C` or `Ctrl+D`.

## Usage Examples
- Set a variable: `x = 5`
- Add two numbers: `res = x + 2`
- Conditional logic: `if x > 5 then y = 1 else y = 0`
- Loop with a block: `while x < 10 do { x = x + 1; y = x * 2; }`

## Design Decisions
The language is designed to be simple, emphasizing clarity and ease of understanding over advanced features. The interpreter is written in Python, chosen for its readability and extensive standard library.

## Limitations
- The language only supports integer arithmetic.
- Recursion and complex data types like arrays or objects are not supported.

## Acknowledgements
- Dr. Sharon Yalov-Handzel, for guidance and course materials.
- Open-source projects that inspired the design and implementation of this interpreter.

