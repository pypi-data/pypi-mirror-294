Interpreter for the Lox programming language

# Getting Started

`pip install pplox`

Create your lox file. For example, `hello_world.lox` 

```
print "Hello world"
```

Tokenize the file with `pplox --tokenize hello_world.lox`.

Parse the file with `pplox --parse hello_world.lox`.

See the [documentation](https://pplox.readthedocs.io/en/latest/) for more details.

# Library Usage
pplox can also be used as a library in your own Python projects.
For example, if you want to implement your own Lox interpreter but want to skip writing the scanner, you can use pplox' scanner like so:
```python
from pplox.scanner import Scanner

scanner = Scanner('print "Hello world"')
tokens = scanner.scan_tokens()
```
This gives you a list of tokens to be parsed and interpreted.

See https://github.com/karlcaga/pplox_web/ for an example application of pplox being used as a library.