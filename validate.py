operators = ["AND", "OR", "IF_THEN", "IF_AND_ONLY_THEN"]
constants = ["TRUE", "FALSE"]
gramatic = {
    "PROPOSITIONAL_VAR": ["OPERATOR", "LPAREN", "RPAREN"],
    "TRUE": ["OPERATOR", "LPAREN", "RPAREN"],
    "FALSE": ["OPERATOR", "LPAREN", "RPAREN"],
    "OPERATOR": constants + ["PROPOSITIONAL_VAR", "NOT", "LPAREN"],
    "NOT": ["NOT", "PROPOSITIONAL_VAR", "LPAREN"] + constants,
    "": ["NOT", "PROPOSITIONAL_VAR", "LPAREN"] + constants,
    "LPAREN": ["LPAREN", "PROPOSITIONAL_VAR", "NOT"] + constants,
    "RPAREN": ["RPAREN", "LPAREN", "PROPOSITIONAL_VAR", "OPERATOR"] + constants,
    "END": ["TRUE", "FALSE", "PROPOSITIONAL_VAR", "RPAREN"]
}

operators_values = {
    "o": "or", "^": "and", "=>" : "si", "<=>": "si y solo si"
}


def invalidParentesisCount(data):

    string = f'''{data}'''
    string.replace(" ", "")


    parentesisCounter = 0
    for char in string:
        if str(char) == "(":
            parentesisCounter += 1
        elif str(char) == ")":
            parentesisCounter -= 1
        if parentesisCounter < 0:
            return True

    if parentesisCounter != 0:
        return True
    return False

def checkGramatic(value, expression):
    if len(expression) == 0:
        return value in gramatic[""]
    else:
        return value in gramatic[expression[len(expression) - 1].type]


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





