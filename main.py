import ply.lex as lex
import ply.yacc as yacc
import networkx as nx
from validate import checkGramatic, gramatic, dump_expression
import matplotlib.pyplot as plt

from validate import invalidParentesisCount

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
t_PROPOSITIONAL_VAR = r'[p-z]'

# t_PROPOSITIONAL_VAR = r'p|q|r|s|t|u|v|w|x|y|z'

t_TRUE = r'1'
t_FALSE = r'0'
t_NOT = r'\~'
t_OPERATOR = r'\^|=>|<=>|o'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    raise Exception("Caracter ilegal '%s'" % t.value[0])


def p_calc(p):
    '''
        calc : expression
        | empty
    '''
    p[0] = p[1]


def p_empty(p):
    '''
    empty :
    '''


def p_expression(p):
    '''
    expression : expression OPERATOR expression
    '''
    p[0] = (p[1], p[2], p[3])


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


def draw_tree(branch, parent, tree_graph, epoch):
    if len(branch) == 3:
        left_leaf, stick, right_leaf = branch
        draw_tree((left_leaf, stick), parent, tree_graph, epoch / 2)
        draw_tree((right_leaf, stick), parent, tree_graph, epoch / 2)
    elif len(branch) == 2:
        leaf, stick = branch

        if type(leaf) == tuple:
            graph.add_edge(parent, stick, weight=epoch)
            graph.add_edge(stick, leaf, weight=epoch)
            draw_tree(leaf, leaf, tree_graph, epoch / 2)

        elif type(stick) == tuple:
            graph.add_edge(parent, leaf, weight=epoch)
            graph.add_edge(leaf, leaf, weight=epoch)
            draw_tree(stick, leaf, tree_graph, epoch / 2)

        else:
            graph.add_edge(parent, stick, weight=epoch)
            graph.add_edge(stick, leaf, weight=epoch)
    else:
        graph.add_edge(branch, branch)


lexer = lex.lex()
tests = [
    'p',
    '~~~q',
    '(p^q)',
    '~(p^q)',
    '(p<=>~p)',
    '((p=>q)^p)',
    '~(p^(qor))os'
]

for test in tests:
    plt.clf()
    if invalidParentesisCount(test):
        raise Exception("La gramatica no esta correcta")

    lexer.input(test)

    expression = []
    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
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
        tree = parser.parse(test)
        break

    print(dump_expression(expression))
    graph = nx.DiGraph()

    draw_tree(tree, tree, graph, 10)
    pos = nx.kamada_kawai_layout(graph)
    nx.draw(graph, with_labels=True, pos=pos)

    plt.show()
    graph = None
