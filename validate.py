
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






