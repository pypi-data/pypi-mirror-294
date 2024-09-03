
class Visitor:
    def visit_print(self, stmt):
        ...

    def visit_expression(self, stmt):
        ...
    
    def visit_var_stmt(self, stmt):
        ...

class Stmt:
    def accept(self, visitor):
        ...

class VarStmt(Stmt):
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor):
        return visitor.visit_var_stmt(self)
    
class Expression(Stmt):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_expression(self)

class Print(Stmt):
    def __init__(self, expression):
        self.expression = expression
    
    def accept(self, visitor):
        return visitor.visit_print(self)
