class Expression(object):
    def __init__(self, tokens, expression):
        self.expression = expression
        self.expressions_branches = []
        self.tree = None
        self.tokens = tokens



