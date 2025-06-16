class _Prompt:
    def __init__(self, value=None):
        self._value = value
    def ask(self):
        return self._value

def select(question, choices=None):
    return _Prompt(choices[0] if choices else None)

def text(question, default=None):
    return _Prompt(default)

def confirm(question, default=False):
    return _Prompt(default)
