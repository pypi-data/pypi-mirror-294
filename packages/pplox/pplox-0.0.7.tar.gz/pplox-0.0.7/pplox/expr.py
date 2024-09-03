
class Visitor:
    def visit_literal(self, expr):
        ...    
    def visit_grouping(self, expr):
        ...
    def visit_unary(self,expr):
        ...
    def visit_binary(self, expr):
        ...
    def visit_variable_expr(self, expr):
        ...

class Expr:
    def accept(self, visitor):
        ...
    
class Assign(Expr):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_assign(self)

class VariableExpr(Expr):
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_variable_expr(self)

class Literal(Expr):
    def __init__(self, value):
        self.value = value
    
    def accept(self, visitor):
        return visitor.visit_literal(self)
        
class Grouping(Expr):
    def __init__(self, expression):
        self.expression = expression
    def accept(self, visitor):
        return visitor.visit_grouping(self)
    
class Unary(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_unary(self)

class Binary(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary(self)