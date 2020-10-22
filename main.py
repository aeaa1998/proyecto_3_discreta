from parser import *

menu_options = ["Ingresar data", "Salir"]
menu_options_2 = ["Ver Grafo", "Ver la expresion", "Salir"]

while True:
    d = selectOptionInList("Ingrese que opcion desea usar", menu_options)
    if d == 0:
        data = input("Ingrese su expresion\n")
        d2 = selectOptionInList("Ingrese que opcion desea usar", menu_options_2)
        if d2 == 0:
            print_graph(data)
        elif d2 == 1:
            print_expression(data)
        break
    else:
        break