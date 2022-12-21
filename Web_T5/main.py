from fastapi import FastAPI
import util_methods as util
import wikipedia
import requests
import math

app = FastAPI()
dirUrl = 'https://api.adamix.net/apec/cedula/'
urlZ = 'https://api.xor.cl/tyaas/'
person = {
    'Nombre': str,
    'Apellido': str,
    'Signo': str,
    'Edad': int
}


@app.get('/')
def index():
    return {
        'Tarea': 'Numero 5',
        'Metodos': {
            'p1': 'Aceptar 2 numeros y mostrar el resultado de la suma.',
            'p2': 'Aceptar una cedula y mostrar nombre, apellido, el signo del zodiaco y la edad de la persona.',
            'p3': 'Aceptar un numero, mostrar ese numero en letra en español del 1 al 1000',
            'p4': 'Aceptar varios números separados por coma, encontrar el mayor de estos.',
            'p5': 'Aceptar una palabra, determinar cuantas vocales y consonantes tiene la misma.',
            'p6': 'Aceptar un salario mensual de un empleado, determinar el impuesto sobre la renta.',
            'p7': 'Aceptar una nota, mostrar el equivalente literal. A, B, C o F.',
            'p8': 'Aceptar una palabra o frase, retornar el resumen de esta según la wikipedia.',
            'p9': 'Aceptar 2 catetos, retornar la hipotenusa.',
            'p10': ' Aceptar un signo zodiacal y mostrar retornar el horóscopo correspondiente al día de hoy y sus números de la suerte.' +
                 'Le pueden pasar el nombre del signo o la fecha de nacimiento en formato YYYY-MM-DD'
        }
    }


@app.get('/p1/n1={n1}&n2={n2}')
def punto_1(n1: int, n2: int):
    result = n1 + n2
    return {'Resultado': result}


@app.get('/p2/{cedula}')
def punto_2(cedula: str):
    r = requests.get(dirUrl+cedula)
    nacDate = r.json()['FechaNacimiento'].split(' ')[0]
    nombres = r.json()['Nombres'].split(' ')

    person['Nombre'] = nombres[0].capitalize() + " " + nombres[1].capitalize()
    person['Apellido'] = r.json()['Apellido1'].capitalize() + \
        " " + r.json()['Apellido2'].capitalize()
    person['Edad'] = util.getOld(nacDate)
    person['Signo'] = util.getSign(nacDate)
    return person


@app.get('/p3/{num}')
def punto_3(num: int):
    r = requests.get(f'https://nal.azurewebsites.net/api/NAL?num={num}')
    letras = r.json()['letras']
    return {'Numero en letras': letras.capitalize()}


@app.get('/p4/{nums}')
def punto_4(nums: str):
    arrayNums = []
    arrayStr = nums.split(',')
    for numStr in arrayStr:
        arrayNums.append(int(numStr))
    return {'Mayor': max(arrayNums)}


@app.get('/p5/{word}')
def punto_5(word: str):
    return util.getLetters(word)


@app.get('/p6/{salary}')
def punto_6(salary: float):
    return util.getIRS(float(salary))


@app.get('/p7/{nota}')
def punto_7(nota: int):
    return util.getLiteral(nota)


@app.get('/p8/{search}')
def punto_8(search: str):
    wikipedia.set_lang('es')
    return {'Resultado de busqueda en wikipedia': wikipedia.summary(search)}


@app.get('/p9/c1={c1}&c2={c2}')
def punto_9(c1: int, c2: int):
    a = math.pow(c1, 2)
    b = math.pow(c2, 2)
    c = math.sqrt(a+b)
    return {'Cateto a': c1, 'Cateto b': c2, 'Hipotenusa': round(c, 2)}


@app.get('/p10/{zodiac}')
def punto_10(zodiac: str):
    r = requests.get(urlZ).json()
    result = util.Zod_or_Date(zodiac.lower())
    date_today = util.todayDate(r['titulo'])
    return {'Fecha': date_today, 'Horoscopo': r['horoscopo'][result]}
