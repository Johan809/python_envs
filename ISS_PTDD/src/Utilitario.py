"""
a. Que reciba un número entero y devuelva si el número es primo o no.
b. Que reciba una fecha de nacimiento de una persona y devuelva la edad de acuerdo a esa fecha.
c. Que reciba un salario bruto y determine el salario neto, para lo cual descontará un 25% de impuesto 
    y al monto que quede le descontará un 3.04 % de ARS y 2.87% de AFP.
"""
import math
from datetime import datetime


def is_Prime(num: int):
    if (num <= 1):
        return False

    for i in range(2, math.ceil(math.sqrt(num))+1):
        if (num % i == 0 and i != num):
            return False

    return True


def getOld(nacDate: str):
    today = datetime.now()
    birthday = datetime.strptime(nacDate, "%Y-%m-%d")
    return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))


def netSal(salary: int):
    taxes = salary * 0.25
    rest = salary - taxes
    ars = rest * 0.0304
    afp = rest * 0.0287
    return rest - ars - afp
