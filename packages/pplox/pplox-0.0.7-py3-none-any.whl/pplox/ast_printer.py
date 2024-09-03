from .expr import Visitor

class AstPrinter(Visitor):
    def print (self, expr):
        return expr.accept(self)
    
    def visit_literal(self, expr):
        if expr.value is None:
            return 'nil'
        if isinstance(expr.value, bool):
            if expr.value:
                return 'true'
            return 'false'
        return str(expr.value)
        
    def visit_grouping(self, expr):
        return self.parenthesize("group", expr.expression)
    
    def visit_unary(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.right)
    
    def visit_binary(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)
    
    def parenthesize(self, name, *exprs):
        result = "("
        result += name
        for expr in exprs:
            result += " "
            result += expr.accept(self)
        result += ")"
        return result
    