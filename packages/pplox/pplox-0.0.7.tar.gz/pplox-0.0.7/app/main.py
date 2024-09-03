#!/usr/bin/env python
import sys
from pplox.scanner import Scanner
from pplox.error_reporter import ErrorReporter
from pplox.parser import Parser, ParseError
from pplox.ast_printer import AstPrinter
from pplox.interpreter import Interpreter, to_string
from pplox.interpreter_error import InterpreterError

def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh [tokenize, parse] <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize" and command != "parse" and command != "evaluate" and command != "run":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

    if command == "tokenize":
        scanner = Scanner(file_contents)
        tokens = scanner.scan_tokens()
        for token in tokens:
            print(token.to_string())
    
    if command == "parse":
        scanner = Scanner(file_contents + ";")
        tokens = scanner.scan_tokens()
        try:
            parser = Parser(tokens)
            expr = parser.parse()[0].expression 
            if expr is not None:
                print(AstPrinter().print(expr))
        except ParseError:
            exit(65)
        except IndexError:
            exit(65)

    if command == "evaluate":
        scanner = Scanner(file_contents + ";")
        tokens = scanner.scan_tokens()
        try:
            parser = Parser(tokens)
            expr = parser.parse()[0].expression
            if expr is not None:
                try:
                    print(to_string(Interpreter().evaluate(expr)))
                except InterpreterError as e:
                    print(e, file = sys.stderr)
                    exit(70)
        except ParseError:
            exit(65)
        except IndexError:
            exit(65)
            
    if command == "run":
        scanner = Scanner(file_contents)
        tokens = scanner.scan_tokens()
        try:
            parser = Parser(tokens)
            statements = parser.parse()
            if statements:
                try:
                    Interpreter().interpret(statements)
                except InterpreterError as e:
                    print(e, file = sys.stderr)
                    exit(70)
        except ParseError:
            exit(65)

    if ErrorReporter.had_error:
        exit(65)
        
    if ErrorReporter.had_runtime_error:
        exit(70)

if __name__ == "__main__":
    main()
