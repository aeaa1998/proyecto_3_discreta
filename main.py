import ply.lex as lex
import re
from validate import invalidParentesisCount
import functools
from itertools import permutations, product
from expression import Expression
import  inspect

tokens = (
    'PROPOSITIONAL_VAR',
    "NOT",
    "OPERATOR",
    # "AND",
    # "OR",
    # "IF_THEN",
    # "IF_AND_ONLY_THEN",
    "TRUE",
    "FALSE",
    'LPAREN',
    'RPAREN'
)

t_PROPOSITIONAL_VAR = r'p|q|r|s|t|u|v|w|x|y|z'
t_TRUE = r'1'
t_FALSE = r'0'
t_NOT = r'\~'
t_OPERATOR = r'\~|\^|=>|<=>'
# t_AND = r'\^'
# t_OR = r'o'
# t_IF_THEN = r'=>'
# t_IF_AND_ONLY_THEN = r'^<=>$'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ignore = ' \t'

operators = ["AND", "OR", "IF_THEN", "IF_AND_ONLY_THEN"]
constants = ["TRUE", "FALSE"]
gramatic = {
    "PROPOSITIONAL_VAR": ["OPERATOR", "LPAREN", "RPAREN"],
    "TRUE": ["OPERATOR", "LPAREN", "RPAREN"],
    "FALSE": ["OPERATOR", "LPAREN", "RPAREN"],
    "OPERATOR": constants + ["PROPOSITIONAL_VAR", "NOT", "LPAREN"],
    "NOT": ["NOT", "PROPOSITIONAL_VAR", "LPAREN"] + constants,
    "": ["NOT", "PROPOSITIONAL_VAR", "LPAREN"] + constants,
    "LPAREN": ["LPAREN", "PROPOSITIONAL_VAR"] + constants,
    "RPAREN": ["RPAREN", "LPAREN", "PROPOSITIONAL_VAR", "OPERATOR"] + constants,
    "END": ["TRUE", "FALSE", "PROPOSITIONAL_VAR", "RPAREN"]
}

operators_values = {
    "o": "or", "^": "and", "=>" : "si", "<=>": "si y solo si"
}


expression = []
def checkGramatic(value):
    if len(expression) == 0:
        return value in gramatic[""]
    else:
        return value in gramatic[expression[len(expression) - 1].type]


expressionPermutations = product(["PROPOSITIONAL_VAR", "TRUE", "FALSE", "E"], repeat = 2)
validExpressions = ["NOT PROPOSITIONAL_VAR", "NOT TRUE", "NOT FALSE", "NOT E"]
for tuple in expressionPermutations:
    validExpressions.append(tuple[0]+" OPERATOR "+tuple[1])

def findClosingParentesis(tokens):
    count = 0
    i = 0
    for tok in tokens:
        if tok.type == "LPAREN":
            count+=1
        elif tok.type == "RPAREN":
            count -= 1
        if count == 0:
            return i
        i+=1

def find_next_var(tokens):
    count = 0
    i = 0
    for tok in tokens:
        if tok.type != "NOT":
            return i
        i+=1

def recursiveResolveNot(tokens, carry, strHolder, parentesisValue=None):

    for tok in tokens:
        if tok.type == "LPAREN":
            return Expression([carry, parentesisValue], "~E")
        if tok.type != "NOT":
            return Expression([carry, tok], "~"+tok.type)
        else:
            return Expression([carry, recursiveResolveNot([tokens[x] for x in range(1, len(tokens) - 1)], tok, "~", parentesisValue)], strHolder)



def evaluateExpressions(tokens, initialVal=""):
    stringExpression = initialVal
    index = 0
    pointer  = 0
    currentExpression = None
    if len(tokens) == 1:
        return Expression(tokens[0], tokens[0].type)
    while index < len(tokens):
        tok = tokens[index]
        if isinstance(tok, Expression):
            if index == 0:
                stringExpression += "E"
            else:
                stringExpression += " E"
            for validExpression in validExpressions:
                if validExpression in stringExpression:
                    if currentExpression is None:
                        currentExpression = Expression([x for x in tokens], stringExpression)
                    else:
                        collapsedExpression = evaluateExpressions([tokens[t] for t in range(pointer + 1, index + 1)])
                        currentExpression = Expression([currentExpression, collapsedExpression], stringExpression)
                    stringExpression.replace(validExpression, "E", 1)
                    pointer = index
                    break

        elif tok.type == "NOT":
            end = find_next_var([tokens[x] for x in range(index+1, len(tokens) - 1)])
            if tokens[end] != "LPAREN":
                index = end + 1
                expressionHolder = recursiveResolveNot([tokens[x] for x in range(index+1, end + 1)], tok, "~")
                if currentExpression is None:
                    currentExpression = expressionHolder
                else:
                    currentExpression = Expression([currentExpression, expressionHolder], stringExpression)
            else:
                tokensInRange = [tokens[t] for t in range(end, len(tokens))]
                endParentesis = findClosingParentesis(tokensInRange)
                parentesisExpression = evaluateExpressions([tokens[t] for t in range(end + 1, endParentesis)])
                index = endParentesis + 1
                expressionHolder = recursiveResolveNot([tokens[x] for x in range(index + 1, end + 1)], tok, "~", parentesisExpression)
                if currentExpression is None:
                    currentExpression = expressionHolder
                else:
                    currentExpression = Expression([currentExpression, expressionHolder], stringExpression)

        elif tok.type != "LPAREN":
            if index == 0:
                stringExpression += tok.type
            else:
                stringExpression += " " + tok.type

            for validExpression in validExpressions:
                if validExpression in stringExpression:
                    if currentExpression is None:
                        currentExpression = Expression([x for x in tokens], stringExpression)
                    else:
                        collapsedExpression = evaluateExpressions([tokens[t] for t in range(pointer + 1, index + 1)])
                        currentExpression = Expression([currentExpression, collapsedExpression], stringExpression)
                    stringExpression.replace(validExpression, "E", 1)
                    pointer = index
                    break
        else:
            tokensInRange = [tokens[t] for t in range(index, len(tokens))]
            end = index + findClosingParentesis(tokensInRange)
            parentesisExpression = evaluateExpressions([tokens[t] for t in range(index+1, end)])
            if currentExpression is None:
                currentExpression = Expression([evaluateExpressions([tokens[t] for t in range(0, index)] + [parentesisExpression])], stringExpression)
            else:
                currentExpression = Expression([currentExpression, parentesisExpression], stringExpression)
            index = end
        index += 1
    return currentExpression


def dump_expression(tokens):
    string = ""
    for index, token in enumerate(tokens):
        if token.type=="OPERATOR":
            if index == 0:
                string += operators_values[token.value]
            else:
                string += " " + operators_values[token.value]
        elif token.type == "PROPOSITIONAL_VAR" or token.type == "LPAREN" or token.type == "RPAREN":
            if index == 0:
                string += token.value
            else:
                string += " " + token.value
        else:
            if index == 0:
                string += token.type
            else:
                string += " " + token.type
    return string

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    raise Exception("Caracter ilegal '%s'" % t.value[0])



lexer = lex.lex()

data = '''0=>(1^p)'''

if invalidParentesisCount(data):
    raise Exception("La gramatica no esta correcta")

lexer.input(data)

toks = []
# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        if expression[len(expression) -1] not in gramatic["END"]:
            break  # No more input
        else:
            raise Exception("La gramatica no esta correcta")
    if checkGramatic(tok.type):
        expression.append(tok)
    else:
        raise Exception("La gramatica no esta correcta ", tok.type)

    print("type ", tok.type, "value: ", tok.value, "libeo: ", tok.lineno, "lexpos: ", tok.lexpos)

print(expression)
tree = evaluateExpressions(expression)
#FALTA SOLOP ASEGURARSE DEL ARBOLITO
print(tree)
# INCISO 5 hecho solo es esto!!
print(dump_expression(expression))



