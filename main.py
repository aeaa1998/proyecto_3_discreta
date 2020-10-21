import ply.lex as lex
import ply.yacc as yacc
import networkx as nx
from validate import checkGramatic, gramatic, dump_expression
import matplotlib.pyplot as plt
import itertools

import re
from validate import invalidParentesisCount
import uuid

tokens = (
    'PROPOSITIONAL_VAR',
    "NOT",
    "OPERATOR",
    "TRUE",
    "FALSE",
    'LPAREN',
    'RPAREN'
)

# t_EXPRESSION = r'([p-z]|[0-1])(\~|\^|=>|<=>|o)([p-z]|[0-1])'
t_PROPOSITIONAL_VAR = r'p|q|r|s|t|u|v|w|x|y|z'
t_TRUE = r'1'
t_FALSE = r'0'
t_NOT = r'\~'
t_OPERATOR = r'\^|=>|<=>|o'
# t_AND = r'\^'
# t_OR = r'o'
# t_IF_THEN = r'=>'
# t_IF_AND_ONLY_THEN = r'^<=>$'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    raise Exception("Caracter ilegal '%s'" % t.value[0])






operators_values = {
    "o": "or", "^": "and", "=>" : "si", "<=>": "si y solo si"
}


lexer = lex.lex()



# data = '''~~~1o~~(po0)^1'''
data = '''~~~1o0'''



if invalidParentesisCount(data):
    raise Exception("La gramatica no esta correcta")

lexer.input(data)

expression = []
toks = []
# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        if expression[len(expression) -1] not in gramatic["END"]:
            break  # No more input
        else:
            raise Exception("La gramatica no esta correcta")
    if checkGramatic(tok.type, expression):
        expression.append(tok)
    else:
        raise Exception("La gramatica no esta correcta ", tok.type)




def p_calc(p):
    '''
        calc : expression
        | empty
    '''
    print(p[1])
    p[0] = p[1]

def p_empty(p):
    '''
    empty :
    '''

def p_expression(p):
    '''
    expression : expression OPERATOR expression
    '''
    p[0] = (p[2], p[1], p[3])

def p_expression_negated(p):
    '''
    expression_negated : NOT PROPOSITIONAL_VAR
    | NOT TRUE
    | NOT FALSE
    | NOT expression
    | NOT expression_negated
    '''
    p[0] = (p[1], p[2])

def p_expression_simple(p):
    '''
    expression : PROPOSITIONAL_VAR
    | TRUE
    | FALSE
    | expression
    | expression_negated
    '''
    p[0] = (p[1])

def p_expression_parentesis(p):
    '''
    expression : LPAREN expression RPAREN
    '''
    p[0] = p[2]


def p_error(p):
    print(p)
    print("Syntax error in input!")

    # Build the parser


parser = yacc.yacc()


while True:
    tree = parser.parse(data)
    break




def get_top(tree):
    if len(tree) == 3:
        operator, left, right = tree
        return operator
    elif len(tree) == 2:
        operator, expression = tree
        return operator

def add_expression(graph, expression, operator):
    if type(expression) == tuple:
        graph.add_edge(operator, get_top(expression))
        add_edges(graph, expression)
    else:
        graph.add_edge(operator, expression)

def add_edges(graph, tree):
    if len(tree) == 3:
        operator, left, right = tree
        add_expression(graph, right, operator)
        add_expression(graph, left, operator)


    elif len(tree) == 2:
        operator, expression = tree
        add_expression(graph, expression, operator)


print(dump_expression(expression))

    # try:
    #     left,right = tree
    # except ValueError:
    #     return
    # graph.add_edge(tree,left)
    # graph.add_edge(tree,right)
    # add_edges(graph,left)
    # add_edges(graph,right)
graph = nx.DiGraph()
labels = {}

# for item in flat_list_var:
#     labels[item["id"]] = item["value"]

add_edges(graph,tree)
# merged = list(itertools.chain.from_iterable(tree))
# graph.add_edges_from(tree)
# for node in graph.nodes():
#     graph.nodes[node]['label'] = labels[str(node)]
nx.draw(graph, with_labels = True)
# pos = nx.nx_pydot.pydot_layout(graph, prog='dot')
# nx.draw_networkx(graph, pos,True, True, with_labels={'o': 'OR', '~': 'NOT', '1': 'TRUE', '0': 'FALSE'})

plt.savefig("filename.png")
