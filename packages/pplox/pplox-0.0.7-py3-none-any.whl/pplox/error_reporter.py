import sys

class ErrorReporter:
    had_error = False
    had_runtime_error = False
    
    @classmethod
    def error(cls, line, message):
        cls.report(line, "", message)
    
    @classmethod
    def runtime_error(cls, error):
        print(str(error) + "\n[line " + str(error.token.line) + "]", file=sys.stderr)
        cls.had_runtime_error = True

    @classmethod
    def report(cls, line, where, message):
        print("[line " + str(line) + "] Error" + where + ": " + message, file=sys.stderr)
        cls.had_error = True
           
