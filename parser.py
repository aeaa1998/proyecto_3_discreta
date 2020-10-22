import ply.lex as lex
import ply.yacc as yacc
import networkx as nx
from validate import checkGramatic, gramatic, dump_expression
import matplotlib.pyplot as plt
import random
import itertools
from utils import  *

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
# data = '''~1o~~p^q'''



# if invalidParentesisCount(data):
#     raise Exception("La gramatica no esta correcta")





ids= {}
def parse_expression(val):
    # return val
    if type(val) == tuple or type(val) == list:
        return parse_tuples(val)
    if val not in ids.keys():
        id = uuid.uuid4().hex
        ids[id] = val
        return id
    return val


def parse_tuples(tuples):
    idsList =[]
    # return tuples
    for item in tuples:
        if type(item) == tuple or type(item) == list:
            idsList.append(item)
        else:
            if item not in ids.keys():
                id = uuid.uuid4().hex
                idsList.append(id)
                ids[id] = item
            else:
                idsList.append(item)
    return idsList



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
    | expression OPERATOR PROPOSITIONAL_VAR
    | expression OPERATOR TRUE
    | expression OPERATOR FALSE
    '''
    p[0] = parse_tuples((p[2], p[1], p[3]))

def p_expression_negated(p):
    '''
    expression_negated : NOT expression
    | NOT expression_negated
    | NOT TRUE
    | NOT FALSE
    | NOT expression_paren
    | NOT PROPOSITIONAL_VAR
    '''
    p[0] = parse_tuples((p[1], p[2]))

def p_expression_simple(p):
    '''
    expression : PROPOSITIONAL_VAR
    | TRUE
    | FALSE
    | expression_negated
    | expression_paren
    | expression
    '''
    p[0] = parse_expression(p[1])

def p_expression_parentesis(p):
    '''
    expression_paren : LPAREN expression RPAREN
    '''
    p[0] = p[2]


def p_error(p):
    print(p)
    print("Syntax error in input!")

    # Build the parser







def get_top(tree):
    if len(tree) == 3:
        operator, left, right = tree
        return operator
    elif len(tree) == 2:
        operator, expression = tree
        return operator
    elif len(tree) == 1:
        operator = tree
        return operator

def add_expression(graph, expression, operator):
    if type(expression) == tuple or type(expression) == list:
        if len(expression) > 1:
            graph.add_edge(operator, get_top(expression))
            add_edges(graph, expression)
        else:
            graph.add_edge(operator, expression[0])
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
    elif len(tree) == 1:
        operator, expression = tree
        add_expression(graph, expression, operator)





expression = []
toks = []
# Tokenize


def print_expression(data):
    expression = []
    ids = {}
    lexer.input(data)
    while True:

        tok = lexer.token()
        if not tok:
            if len(expression) == 0:
                return
            if expression[len(expression) - 1] not in gramatic["END"]:
                break  # No more input
            else:
                raise Exception("La gramatica no esta correcta")
        if checkGramatic(tok.type, expression):
            expression.append(tok)
        else:
            raise Exception("La gramatica no esta correcta ", tok.type)
    print(dump_expression(expression))

def print_graph(data):
    expression = []
    lexer.input(data)
    while True:

        tok = lexer.token()
        if not tok:
            if len(expression) == 0:
                return
            if expression[len(expression) - 1] not in gramatic["END"]:
                break  # No more input
            else:
                raise Exception("La gramatica no esta correcta")
        if checkGramatic(tok.type, expression):
            expression.append(tok)
        else:
            raise Exception("La gramatica no esta correcta ", tok.type)
    parser = yacc.yacc()

    while True:
        tree = parser.parse(data)
        break



    graph = nx.DiGraph(directed=True)
    ids[data] = data

    add_edges(graph,tree)
    graph.add_edge(data, get_top(tree))


    list_colors = ['r','b','y','c']
    colors = []
    for node in graph.nodes():
        colors.append(list_colors[random.randint(0 , len(list_colors) - 1)])



    options = {
        'node_size': 450,
        'arrowstyle': '-|>',
        'arrowsize': 12,
    }
    # nx.draw_networkx(graph, labels=ids, with_labels = True, arrows=True, node_color=colors, **options)
    nx.draw(graph, labels=ids, with_labels = True, arrows=True, node_color=colors, **options)
    # pos = nx.nx_pydot.pydot_layout(graph, prog='dot')
    # nx.draw_networkx(graph, pos,True, True, with_labels={'o': 'OR', '~': 'NOT', '1': 'TRUE', '0': 'FALSE'})
    # plt.show()
    plt.savefig("filename.png")





