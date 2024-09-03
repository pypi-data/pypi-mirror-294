from pplox.parser import Parser 
from pplox.scanner import Scanner
from pplox.expr import Literal

def parse(source):
    scanner = Scanner(source + ";")
    tokens = scanner.scan_tokens()
    parser = Parser(tokens)
    return parser.parse()[0].expression

def test_boolean_nil():
    assert parse('true').value == Literal(True).value
    assert parse('false').value == Literal(False).value
    assert parse('nil').value == Literal(None).value

def test_number():
    assert parse("42.47").value == Literal(42.47).value

def test_string():
    assert parse('"hello"').value == Literal("hello").value

def test_paren():
    assert parse ('("foo")').expression.value == Literal("foo").value

def test_unary():
    result = parse("!true")
    assert result.operator.lexeme == "!"
    assert result.right.value == Literal(True).value

def test_binary():
    binary = parse("16 * 38")
    assert binary.operator.lexeme == "*"
    assert binary.left.value == Literal(16).value
    assert binary.right.value == Literal(38).value

def test_term():
    term = parse("1 + 2 - 3")

    assert term.operator.lexeme == "-"
    assert term.right.value == Literal(3).value
    assert term.left.operator.lexeme == "+"
    assert term.left.left.value == Literal(1).value
    assert term.left.right.value == Literal(2).value 

def test_less_than():
    less_than_compare = parse("1 < 2 <= 3")

    assert less_than_compare.operator.lexeme == "<="
    assert less_than_compare.right.value == Literal(3).value
    assert less_than_compare.left.operator.lexeme == "<"
    assert less_than_compare.left.left.value == Literal(1).value
    assert less_than_compare.left.right.value == Literal(2).value

def test_greater_than():
    greater_than_compare = parse("1 > 2 >= 3")

    assert greater_than_compare.operator.lexeme == ">="
    assert greater_than_compare.right.value == Literal(3).value
    assert greater_than_compare.left.operator.lexeme == ">"
    assert greater_than_compare.left.left.value == Literal(1).value
    assert greater_than_compare.left.right.value == Literal(2).value

def test_equality():
    equality = parse('"1" == "foo"')
    assert equality.operator.lexeme =="=="
    assert equality.left.value == Literal("1").value
    assert equality.right.value == Literal("foo").value
