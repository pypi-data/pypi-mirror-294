from .expr import Visitor 
from .token_type import TokenType
from .interpreter_error import InterpreterError
from . import stmt
from .error_reporter import ErrorReporter
from .environment import Environment

def to_string(val):
    if val is None:
        return 'nil'
    if isinstance(val, bool):
        if val:
            return 'true'
        return 'false'
    if isinstance(val, float):
        text = str(val)
        if text.endswith(".0"):
            text = text[:-2]
        return text
    return str(val)

class Interpreter(Visitor, stmt.Visitor):
    def __init__(self):
        self.environment = Environment()
                
    def interpret(self, statements):
        try:
            for statement in statements:
                self.execute(statement)
        except InterpreterError as e:
            ErrorReporter.runtime_error(e)
    
    def evaluate(self, expr): 
        return expr.accept(self)
    
    def execute(self, stmt):
        stmt.accept(self)
    
    def visit_print(self, stmt):
        value = self.evaluate(stmt.expression)
        print(to_string(value))
        return None
    
    def visit_var_stmt(self, stmt):
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)
        return None
    
    def visit_assign(self, expr):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value
    
    def visit_expression(self, stmt):
        self.evaluate(stmt.expression)
        return None

    def visit_literal(self, expr):
        return expr.value   
    
    def visit_grouping(self, expr):
        return self.evaluate(expr.expression)
    
    def visit_unary(self, expr):
        right = self.evaluate(expr.right)
        match expr.operator.type:
            case TokenType.MINUS:
                self.check_number_operand(expr.operator, right)
                return -(float(right))
            case TokenType.BANG:
                return not self.is_truthy(right)

    def visit_variable_expr(self, expr):
        return self.environment.get(expr.name)

    def visit_binary(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        match expr.operator.type:
            case TokenType.SLASH:
                self.check_number_operands(expr.operator, left, right)
                return float(left) / float(right)
            case TokenType.STAR:
                self.check_number_operands(expr.operator, left, right)
                return float(left) * float(right)
            case TokenType.MINUS:
                self.check_number_operands(expr.operator, left, right)
                return float(left) - float(right)
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) + float(right)
                if isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)
                raise InterpreterError(expr.operator, "Operands must be two numbers or two strings.")
            case TokenType.GREATER:
                self.check_number_operands(expr.operator, left, right)
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return float(left) >= float(right)
            case TokenType.LESS:
                self.check_number_operands(expr.operator, left, right)
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return float(left) <= float(right)
            case TokenType.BANG_EQUAL:
                return not self.is_equal(left, right)
            case TokenType.EQUAL_EQUAL:
                return self.is_equal(left, right)

    def check_number_operand(self, operator, operand):
        if isinstance(operand, float):
            return
        raise InterpreterError(operator, "Operand must be a number.")

    def check_number_operands(self, operator, left, right):
        if isinstance(left, float) and isinstance(right, float):
            return
        raise InterpreterError(operator, "Operands must be numbers.")

    def is_equal(self, a, b):
        if a is None and b is None:
            return True
        if a is None:
            return False
        return a == b
    
    def is_truthy(self, obj):
        if obj is None:
            return False
        if isinstance(obj, bool):
            return bool(obj)
        return True