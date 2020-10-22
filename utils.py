
import re

from typing import Union, List

def intInput(text: str, sign: str = "=", limit: int = 0):
    while True:
        c = input(text + "\n")
        try:
            c = int(c)
            if sign == "=":
                return c
            elif sign == "+" and c > limit:
                return c
            elif sign == "-" and c < limit:
                return c
            print("Ingrese un valor que cumpla con el criterio solicitado.")
        except:
            print("Ingrese un valor valido.")

def intPositiveInput(text: str, limit: int = 1):
    while True:
        c = input(text + "\n")
        try:
            c = int(c)
            if 0 < c <= limit:
                return c
            print(f"Ingrese un valor que cumpla con el criterio solicitado. Mayor a 0 y menor o igual a {str(limit)}")
        except:
            print("Ingrese un valor valido.")


def floatInput(text: str, sign: str = "=", limit: float = 0):
    while True:
        c = input(text + "\n")
        try:
            c = float(c)
            if sign == "=":
                return c
            elif sign == "+" and c > limit:
                return c
            elif sign == "-" and c < limit:
                return c
            print("Ingrese un valor que cumpla con el criterio solicitado.")
        except:
            print("Ingrese un valor valido.")


def selectOptionInList(text: str,  options: list, errorString:str = "Ingrese un numero de opcion valido") -> int:
    while True:
        print(text + "\n")
        for index, value in enumerate(options):
            print(str(index + 1) + ") " + str(value))
        c = intInput("Ingrese el numero de la opcion que desea", sign="+")
        if c <= len(options):
            return c - 1
        else:
            print(errorString)




def emailInput(text: str) -> str:
    while True:
        email = input(f"{text}\n")
        if re.match("^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email):
            return email
        else:
            print("Ingrese un email valido.")


def getProductBrands(products: list) -> list:
    filtered = []
    for p in products:
        for b in p.getBrands():
            if b not in filtered:
                filtered.append(b)
    return filtered

def getProductCategories(products: list) -> list:
    filtered = []
    for p in products:
        for b in p.getCategories():
            if b not in filtered:
                filtered.append(b)
    return filtered








